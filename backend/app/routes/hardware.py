# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: API routes for Phase 7 + Phase 8 hardware scan and dual-node handshakes.

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import constants
from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Event, Hub, Parcel
from app.engines.hardware_engine import (
    normalize_hardware_scan_payload,
    build_hardware_context,
    generate_hardware_command,
)
from app.engines.trust_engine import update_hub_trust, get_trust_status
from app.engines.metrics_engine import get_starter_metrics
from app.routes.scan import process_and_broadcast_scan
from app.schemas.hardware_schema import (
    HardwareScanRequest,
    HardwareScanResponse,
    P2PHandshakeRequest,
    P2PHandshakeResponse,
)
from app.schemas.scan_schema import ScanRequest
from app.utils.time_utils import utc_now_iso

router = APIRouter(prefix="/hardware", tags=["hardware"])


@router.post("/scan", response_model=HardwareScanResponse)
async def hardware_scan(payload: HardwareScanRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    hub = db.get(Hub, payload.hub_id)
    if hub is None:
        raise HTTPException(status_code=404, detail="Hub not found")

    # 1. Normalise payload and build context
    normalized = normalize_hardware_scan_payload(payload)
    context = build_hardware_context(payload)

    # 2. Log HARDWARE_SCAN_RECEIVED event
    raw_payload_str = json.dumps(
        {"request": payload.model_dump(), "context": context}
    )
    db.add(
        Event(
            event_type=constants.HARDWARE_SCAN_RECEIVED,
            parcel_id=payload.parcel_id,
            hub_id=payload.hub_id,
            timestamp=utc_now_iso(),
            decision="RECEIVED",
            action="HARDWARE_INGEST",
            severity="info",
            reason=f"Hardware scan received from {payload.scanner_id}.",
            raw_payload=raw_payload_str,
        )
    )
    db.commit()

    # 3. Broadcast hardware_scan_received WebSocket event
    await safe_broadcast(constants.HARDWARE_SCAN_RECEIVED, {
        "parcel_id": payload.parcel_id,
        "hub_id": payload.hub_id,
        "scanner_id": payload.scanner_id,
        "temperature_c": normalized["temperature_c"],
        "tamper": normalized["tamper"]
    })

    # Broadcast BLE and ESP-NOW events if present
    if payload.ble_verified:
        await safe_broadcast(constants.BLE_TAG_DETECTED, {
            "parcel_id": payload.parcel_id,
            "hub_id": payload.hub_id,
            "rssi": payload.ble_rssi_m,
            "temperature_c": payload.ble_temperature_c
        })
    if payload.esp_now_prior_acceptance:
        await safe_broadcast(constants.ESP_NOW_PRIOR_ACCEPTANCE, {
            "parcel_id": payload.parcel_id,
            "hub_id": payload.hub_id,
            "prior_hub": payload.esp_now_prior_hub,
            "trust_delta": payload.esp_now_trust_delta
        })

    # 4. Check if GPS is present
    has_gps = (
        payload.gps is not None
        and payload.gps.lat is not None
        and payload.gps.lng is not None
    )

    if not has_gps:
        reason = "RFID and temperature captured. Awaiting phone GPS proof."
        return {
            "status": "hardware_scan_received",
            "accepted": False,
            "decision": None,
            "action": None,
            "led": None,
            "parcel_id": payload.parcel_id,
            "hub_id": payload.hub_id,
            "requires_gps": True,
            "gps_scan_url": f"/scan/{payload.hub_id}?parcel_id={payload.parcel_id}",
            "immune_checks": None,
            "failed_checks": [],
            "trust_update": None,
            "route_decision": None,
            "hardware_context": context,
            "reason": reason,
            "message": reason,
        }

    # Construct ScanRequest Pydantic model
    scan_request = ScanRequest(
        parcel_id=normalized["parcel_id"],
        hub_id=normalized["hub_id"],
        scanner_id=normalized["scanner_id"],
        rfid_verified=normalized["rfid_verified"],
        qr_verified=normalized["qr_verified"],
        gps=normalized["gps"],
        temperature_c=normalized["temperature_c"],
        carrier_type=normalized["carrier_type"],
        tamper=normalized["tamper"],
        ble_verified=normalized["ble_verified"],
        ble_rssi_m=normalized["ble_rssi_m"],
        esp_now_prior_acceptance=normalized["esp_now_prior_acceptance"],
        esp_now_prior_hub=payload.esp_now_prior_hub,
        esp_now_trust_delta=payload.esp_now_trust_delta,
    )

    # Call process_and_broadcast_scan to run validation
    result = await process_and_broadcast_scan(db, scan_request)

    # Log HARDWARE_SCAN_COMPLETED event
    db.add(
        Event(
            event_type=constants.HARDWARE_SCAN_COMPLETED,
            parcel_id=payload.parcel_id,
            hub_id=payload.hub_id,
            timestamp=utc_now_iso(),
            decision=result["decision"],
            action=result["action"],
            severity="info",
            reason=f"Hardware scan completed. Outcome: {result['decision']}",
            raw_payload=json.dumps(result),
        )
    )
    db.commit()

    # Generate hardware response actuator command
    cmd = generate_hardware_command(
        hub_id=payload.hub_id,
        parcel_id=payload.parcel_id,
        decision=result["decision"],
        led=result["led"],
        reason=result["reason"],
        failed_checks=result.get("failed_checks", []),
    )

    # Broadcast hardware_scan_completed WebSocket event
    await safe_broadcast(constants.HARDWARE_SCAN_COMPLETED, {
        "parcel_id": payload.parcel_id,
        "hub_id": payload.hub_id,
        "decision": result["decision"],
        "led": result["led"],
        "failed_checks": result.get("failed_checks", []),
        "command": cmd
    })

    return {
        "status": "hardware_scan_completed",
        "accepted": result["decision"] == constants.DECISION_ACCEPTED,
        "decision": result["decision"],
        "action": result["action"],
        "led": result["led"],
        "parcel_id": payload.parcel_id,
        "hub_id": payload.hub_id,
        "requires_gps": False,
        "gps_scan_url": None,
        "immune_checks": result["immune_checks"],
        "failed_checks": result.get("failed_checks", []),
        "trust_update": result.get("trust_update"),
        "route_decision": result.get("route_decision"),
        "hardware_context": context,
        "reason": result["reason"],
        "message": result["reason"],
    }


@router.post("/p2p-handshake", response_model=P2PHandshakeResponse)
async def p2p_handshake(payload: P2PHandshakeRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    sender = db.get(Hub, payload.sender_hub)
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender hub not found")

    receiver = db.get(Hub, payload.receiver_hub)
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver hub not found")

    now = payload.timestamp or utc_now_iso()
    raw_payload_str = json.dumps(payload.model_dump())

    # Log P2P handshake event to ledger
    reason = f"ESP-NOW P2P handshake ({payload.message_type}) from {payload.sender_hub} to {payload.receiver_hub}."
    event = Event(
        event_type=constants.P2P_HANDSHAKE,
        parcel_id=payload.parcel_id,
        hub_id=payload.sender_hub,
        timestamp=now,
        decision=payload.message_type,
        action="P2P_HANDSHAKE",
        severity="info",
        reason=reason,
        raw_payload=raw_payload_str,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Update trust score of receiver hub if trust delta is provided
    trust_update = None
    if payload.trust_delta is not None and payload.trust_delta != 0.0:
        trust_update = update_hub_trust(
            db,
            hub_id=payload.receiver_hub,
            decision="P2P_HANDSHAKE",
            failed_checks=[],
            reason=f"ESP-NOW trust update from {payload.sender_hub}.",
            event_id=event.id,
            esp_now_trust_delta=payload.trust_delta,
        )

        # Broadcast trust score updates
        await safe_broadcast(constants.TRUST_UPDATED, {
            "hub_id": payload.receiver_hub,
            "old_score": trust_update["old_score"],
            "new_score": trust_update["new_score"],
            "delta": trust_update["delta"],
            "trust_status": get_trust_status(trust_update["new_score"])
        })
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    # Broadcast P2P Handshake WebSocket event
    await safe_broadcast(constants.P2P_HANDSHAKE, {
        "sender_hub": payload.sender_hub,
        "receiver_hub": payload.receiver_hub,
        "parcel_id": payload.parcel_id,
        "message_type": payload.message_type,
        "trust_delta": payload.trust_delta,
        "failed_check": payload.failed_check,
        "eta_sec": payload.eta_sec,
        "timestamp": now
    })

    return {
        "status": "success",
        "event_id": event.id,
        "sender_hub": payload.sender_hub,
        "receiver_hub": payload.receiver_hub,
        "parcel_id": payload.parcel_id,
        "message_type": payload.message_type,
        "reason": reason,
    }
