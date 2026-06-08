# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: ImmuneNet scan validation API routes.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import constants
from app.db.database import get_db
from app.db.models import Event, Parcel
from app.engines.immune_engine import validate_scan
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


@router.post("", response_model=ScanResponse)
def scan(payload: ScanRequest, db: Session = Depends(get_db)):
    try:
        return validate_scan(db, payload)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/fake", response_model=ScanResponse)
def fake_scan(payload: FakeScanRequest, db: Session = Depends(get_db)):
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
        temperature_c=parcel.current_temperature if parcel.current_temperature is not None else 24.3,
        carrier_type=parcel.carrier_type,
        tamper=False,
    )
    try:
        return validate_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/clone", response_model=ScanResponse)
def clone_scan(payload: CloneScanRequest, db: Session = Depends(get_db)):
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
        return validate_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error


@router.post("/tamper", response_model=ScanResponse)
def tamper_scan(payload: TamperScanRequest, db: Session = Depends(get_db)):
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
        return validate_scan(db, scan_request)
    except ValueError as error:
        raise _handle_error(error) from error
