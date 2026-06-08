# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: ledger API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event
from app.schemas.event_schema import EventsResponse, ParcelEventsResponse

router = APIRouter(prefix="/ledger", tags=["ledger"])


def serialize_event(event: Event) -> dict[str, object]:
    return {
        "id": event.id,
        "event_type": event.event_type,
        "parcel_id": event.parcel_id,
        "hub_id": event.hub_id,
        "timestamp": event.timestamp,
        "gps_lat": event.gps_lat,
        "gps_lng": event.gps_lng,
        "gps_accuracy_m": event.gps_accuracy_m,
        "temperature_c": event.temperature_c,
        "decision": event.decision,
        "action": event.action,
        "severity": event.severity,
        "reason": event.reason,
        "raw_payload": event.raw_payload,
    }


@router.get("/events", response_model=EventsResponse)
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.id.desc()).limit(100).all()
    return {"events": [serialize_event(event) for event in events]}


@router.get("/parcel/{parcel_id}", response_model=ParcelEventsResponse)
def parcel_events(parcel_id: str, db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .filter(Event.parcel_id == parcel_id)
        .order_by(Event.id.desc())
        .all()
    )
    return {"parcel_id": parcel_id, "events": [serialize_event(event) for event in events]}
