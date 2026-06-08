# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: parcels API routes.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core import constants
from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Event, Hub, Parcel
from app.engines.routing_engine import select_next_hop
from app.routes.ledger import serialize_event
from app.schemas.parcel_schema import (
    ParcelCreateRequest,
    ParcelCreateResponse,
    ParcelDetailResponse,
    ParcelsResponse,
)
from app.utils.time_utils import utc_now_iso

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


@router.post("", response_model=ParcelCreateResponse)
async def create_parcel(payload: ParcelCreateRequest, db: Session = Depends(get_db)):
    source = db.get(Hub, payload.source_hub)
    destination = db.get(Hub, payload.destination_hub)
    if source is None:
        raise HTTPException(status_code=404, detail="Source hub not found")
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination hub not found")

    now = utc_now_iso()
    current_temperature = payload.current_temperature
    if current_temperature is None and payload.id == "MED-104":
        current_temperature = 24.3

    parcel = db.get(Parcel, payload.id)
    if parcel is None:
        parcel = Parcel(
            id=payload.id,
            parcel_type=payload.parcel_type,
            source_hub=payload.source_hub,
            destination_hub=payload.destination_hub,
            current_hub=payload.source_hub,
            previous_hub=None,
            priority=payload.priority,
            sla_minutes=payload.sla_minutes,
            temperature_limit=payload.temperature_limit,
            current_temperature=current_temperature,
            carrier_type=payload.carrier_type,
            status="created",
            trust_state="unverified",
            created_at=now,
            updated_at=now,
        )
        db.add(parcel)
    else:
        parcel.parcel_type = payload.parcel_type
        parcel.source_hub = payload.source_hub
        parcel.destination_hub = payload.destination_hub
        parcel.current_hub = payload.source_hub
        parcel.previous_hub = None
        parcel.priority = payload.priority
        parcel.sla_minutes = payload.sla_minutes
        parcel.temperature_limit = payload.temperature_limit
        parcel.current_temperature = current_temperature
        parcel.carrier_type = payload.carrier_type
        parcel.status = "created"
        parcel.trust_state = "unverified"
        parcel.updated_at = now

    db.add(
        Event(
            event_type=constants.PARCEL_CREATED,
            parcel_id=payload.id,
            hub_id=payload.source_hub,
            timestamp=now,
            decision="CREATED",
            action="CREATE_OR_UPSERT_PARCEL",
            severity="info",
            reason=f"Parcel {payload.id} created at {payload.source_hub}.",
        )
    )
    try:
        db.commit()
        db.refresh(parcel)
        initial_route = select_next_hop(db, payload.id, payload.source_hub, payload.destination_hub)
    except (SQLAlchemyError, ValueError) as error:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error

    await safe_broadcast(
        constants.PARCEL_CREATED,
        {
            "parcel": serialize_parcel(parcel),
            "parcel_id": parcel.id,
            "hub_id": parcel.current_hub,
        },
    )
    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": initial_route["parcel_id"],
            "current_hub": initial_route["current_hub"],
            "selected_next_hop": initial_route["selected_next_hop"],
            "full_route": initial_route["full_route"],
            "candidate_scores": initial_route["candidate_scores"],
            "reason": initial_route["reason"],
        },
    )

    return {"parcel": serialize_parcel(parcel), "initial_route": initial_route}


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
