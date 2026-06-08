# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: parcels API routes.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event, Parcel
from app.routes.ledger import serialize_event
from app.schemas.parcel_schema import ParcelDetailResponse, ParcelsResponse

router = APIRouter(prefix="/parcels", tags=["parcels"])


def serialize_parcel(parcel: Parcel) -> dict[str, object]:
    return {
        "id": parcel.id,
        "parcel_type": parcel.parcel_type,
        "source_hub": parcel.source_hub,
        "destination_hub": parcel.destination_hub,
        "current_hub": parcel.current_hub,
        "previous_hub": parcel.previous_hub,
        "priority": parcel.priority,
        "sla_minutes": parcel.sla_minutes,
        "temperature_limit": parcel.temperature_limit,
        "current_temperature": parcel.current_temperature,
        "carrier_type": parcel.carrier_type,
        "status": parcel.status,
        "trust_state": parcel.trust_state,
    }


@router.get("", response_model=ParcelsResponse)
def list_parcels(db: Session = Depends(get_db)):
    parcels = db.query(Parcel).order_by(Parcel.id).all()
    return {"parcels": [serialize_parcel(parcel) for parcel in parcels]}


@router.get("/{parcel_id}", response_model=ParcelDetailResponse)
def get_parcel(parcel_id: str, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    latest_events = (
        db.query(Event)
        .filter(Event.parcel_id == parcel_id)
        .order_by(Event.id.desc())
        .limit(10)
        .all()
    )
    return {"parcel": serialize_parcel(parcel), "latest_events": [serialize_event(event) for event in latest_events]}
