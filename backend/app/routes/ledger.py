# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: ledger API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event
from app.schemas.event_schema import EventsResponse, ParcelEventsResponse

router = APIRouter(prefix="/ledger", tags=["ledger"])


from typing import Optional, Any
import json

from app.core import constants
from app.db.models import RouteDecision, TrustHistory, ImmuneCheck

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
def list_events(
    limit: int = 50,
    event_type: Optional[str] = None,
    parcel_id: Optional[str] = None,
    hub_id: Optional[str] = None,
    decision: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if parcel_id:
        query = query.filter(Event.parcel_id == parcel_id)
    if hub_id:
        query = query.filter(Event.hub_id == hub_id)
    if decision:
        query = query.filter(Event.decision == decision)

    events = query.order_by(Event.id.desc()).limit(limit).all()
    return {"events": [serialize_event(event) for event in events]}


@router.get("/parcel/{parcel_id}", response_model=ParcelEventsResponse)
def parcel_events(parcel_id: str, db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .filter(Event.parcel_id == parcel_id)
        .order_by(Event.id.desc())
        .all()
    )

    event_ids = [e.id for e in events]

    # Query latest route decision
    decision = (
        db.query(RouteDecision)
        .filter(RouteDecision.parcel_id == parcel_id)
        .order_by(RouteDecision.id.desc())
        .first()
    )
    latest_route_dict = None
    if decision:
        def _parse_json(val, fallback):
            if not val:
                return fallback
            try:
                return json.loads(val)
            except Exception:
                return fallback
        latest_route_dict = {
            "id": decision.id,
            "parcel_id": decision.parcel_id,
            "current_hub": decision.current_hub,
            "selected_next_hop": decision.selected_next_hop,
            "full_route": _parse_json(decision.full_route, []),
            "candidate_scores": _parse_json(decision.candidate_scores, []),
            "final_score": decision.final_score,
            "reason": decision.reason,
            "created_at": decision.created_at or "",
        }

    # Query trust-impact events
    trust_events_list = []
    if event_ids:
        th_records = db.query(TrustHistory).filter(TrustHistory.event_id.in_(event_ids)).all()
        trust_events_list = [
            {
                "id": th.id,
                "hub_id": th.hub_id,
                "old_score": th.old_score,
                "new_score": th.new_score,
                "delta": th.delta,
                "reason": th.reason,
                "event_id": th.event_id,
                "timestamp": th.timestamp,
            }
            for th in th_records
        ]

    # Query immune checks
    checks_list = []
    if event_ids:
        ic_records = db.query(ImmuneCheck).filter(ImmuneCheck.event_id.in_(event_ids)).all()
        checks_list = [
            {
                "id": ic.id,
                "event_id": ic.event_id,
                "parcel_id": ic.parcel_id,
                "hub_id": ic.hub_id,
                "geofence": ic.geofence,
                "speed": ic.speed,
                "route_graph": ic.route_graph,
                "clone_scan": ic.clone_scan,
                "cold_chain": ic.cold_chain,
                "tamper": ic.tamper,
                "decision": ic.decision,
                "action": ic.action,
                "reason": ic.reason,
            }
            for ic in ic_records
        ]

    return {
        "parcel_id": parcel_id,
        "events": [serialize_event(event) for event in events],
        "latest_route": latest_route_dict,
        "trust_events": trust_events_list,
        "immune_checks": checks_list,
    }

