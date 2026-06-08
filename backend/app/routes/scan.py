# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: ImmuneNet scan validation API routes.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import constants
from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Event, Parcel
from app.engines.agentops_engine import get_latest_route_for_parcel
from app.engines.immune_engine import validate_scan
from app.engines.metrics_engine import get_starter_metrics
from app.engines.trust_engine import get_trust_status
from app.schemas.scan_schema import (
    CloneScanRequest,
    FakeScanRequest,
    ScanRequest,
    ScanResponse,
    TamperScanRequest,
)
from app.utils.time_utils import utc_now_iso

router = APIRouter(prefix="/scan", tags=["scan"])


def _handle_error(error: ValueError) -> HTTPException:
    message = str(error)
    if message in {"Parcel not found", "Hub not found"}:
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)


async def process_and_broadcast_scan(db: Session, scan_request: ScanRequest) -> dict:
    # 1. Broadcast scan_received immediately
    await safe_broadcast(
        constants.SCAN_RECEIVED,
        {
            "parcel_id": scan_request.parcel_id,
            "hub_id": scan_request.hub_id,
            "scanner_id": scan_request.scanner_id,
            "temperature_c": scan_request.temperature_c,
        },
    )

    # 2. Call validate_scan
    result = validate_scan(db, scan_request)

    # 3. Broadcast based on decision outcome
    decision = result["decision"]
    failed_checks = result.get("failed_checks") or []

    if decision == constants.DECISION_ACCEPTED:
        await safe_broadcast(
            constants.MOVEMENT_ACCEPTED,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "decision": decision,
                "led": result["led"],
                "immune_checks": result["immune_checks"],
                "reason": result["reason"],
            },
        )
        if result.get("route_decision"):
            rd = result["route_decision"]
            await safe_broadcast(
                constants.ROUTE_DECISION,
                {
                    "parcel_id": rd["parcel_id"],
                    "current_hub": rd["current_hub"],
                    "selected_next_hop": rd["selected_next_hop"],
                    "full_route": rd["full_route"],
                    "candidate_scores": rd["candidate_scores"],
                    "reason": rd["reason"],
                },
            )
    elif decision == constants.DECISION_BLOCKED:
        await safe_broadcast(
            constants.IMMUNE_ALERT,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "decision": decision,
                "failed_checks": failed_checks,
                "action": result["action"],
                "reason": result["reason"],
            },
        )
        await safe_broadcast(
            constants.MOVEMENT_BLOCKED,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "failed_checks": failed_checks,
                "reason": result["reason"],
            },
        )
    elif decision == constants.DECISION_WARNING:
        await safe_broadcast(
            constants.MOVEMENT_WARNING,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "failed_checks": failed_checks,
                "reason": result["reason"],
            },
        )
    elif decision == constants.DECISION_REROUTED:
        parcel = db.get(Parcel, result["parcel_id"])
        temp_limit = parcel.temperature_limit if parcel else 25.0
        await safe_broadcast(
            constants.TEMPERATURE_BREACH,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "temperature_c": scan_request.temperature_c,
                "temperature_limit": temp_limit,
                "decision": decision,
                "reason": result["reason"],
            },
        )
        if result.get("route_decision"):
            rd = result["route_decision"]
            await safe_broadcast(
                constants.REROUTE_TRIGGERED,
                {
                    "parcel_id": result["parcel_id"],
                    "old_route": get_latest_route_for_parcel(db, result["parcel_id"]),
                    "new_route": rd["full_route"],
                    "trigger": "temperature_breach",
                },
            )
            await safe_broadcast(
                constants.ROUTE_DECISION,
                {
                    "parcel_id": rd["parcel_id"],
                    "current_hub": rd["current_hub"],
                    "selected_next_hop": rd["selected_next_hop"],
                    "full_route": rd["full_route"],
                    "candidate_scores": rd["candidate_scores"],
                    "reason": rd["reason"],
                },
            )
    elif decision == constants.DECISION_HOLD:
        await safe_broadcast(
            constants.TAMPER_ALERT,
            {
                "parcel_id": result["parcel_id"],
                "hub_id": result["hub_id"],
                "decision": decision,
                "failed_checks": ["tamper"],
                "reason": result["reason"],
            },
        )

    # 4. Broadcast trust_updated if trust_update is present
    if result.get("trust_update") and result["trust_update"] is not None:
        tu = result["trust_update"]
        await safe_broadcast(
            constants.TRUST_UPDATED,
            {
                "hub_id": tu["hub_id"],
                "old_score": tu["old_score"],
                "new_score": tu["new_score"],
                "delta": tu["delta"],
                "trust_status": get_trust_status(tu["new_score"]),
            },
        )

    # 5. Broadcast metrics_updated
    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return result


@router.post("", response_model=ScanResponse)
async def scan(payload: ScanRequest, db: Session = Depends(get_db)):
    try:
        return await process_and_broadcast_scan(db, payload)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/fake", response_model=ScanResponse)
async def fake_scan(payload: FakeScanRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    scan_request = ScanRequest(
        parcel_id=payload.parcel_id,
        hub_id=payload.claimed_hub,
        scanner_id="FAKE-SCANNER",
        rfid_verified=True,
        qr_verified=True,
        gps=payload.fake_gps,
        temperature_c=parcel.current_temperature
        if parcel.current_temperature is not None
        else 24.3,
        carrier_type=parcel.carrier_type,
        tamper=False,
    )
    try:
        return await process_and_broadcast_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/clone", response_model=ScanResponse)
async def clone_scan(payload: CloneScanRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    db.add(
        Event(
            event_type=constants.MOVEMENT_ACCEPTED,
            parcel_id=payload.parcel_id,
            hub_id=payload.first_hub,
            timestamp=utc_now_iso(),
            decision=constants.DECISION_ACCEPTED,
            action=constants.ACTION_UPDATE_LOCATION,
            severity="info",
            reason="Synthetic accepted movement event for clone scan demo.",
        )
    )
    db.commit()
    scan_request = ScanRequest(
        parcel_id=payload.parcel_id,
        hub_id=payload.second_hub,
        scanner_id="CLONE-SCANNER",
        rfid_verified=True,
        qr_verified=True,
        temperature_c=parcel.current_temperature,
        carrier_type=parcel.carrier_type,
        tamper=False,
    )
    try:
        return await process_and_broadcast_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/tamper", response_model=ScanResponse)
async def tamper_scan(payload: TamperScanRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    scan_request = ScanRequest(
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        scanner_id="TAMPER-SCANNER",
        rfid_verified=True,
        qr_verified=True,
        temperature_c=parcel.current_temperature,
        carrier_type=parcel.carrier_type,
        tamper=payload.tamper,
    )
    try:
        return await process_and_broadcast_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error
