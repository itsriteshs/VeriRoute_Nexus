# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: AgentOps autonomous disruption handling and route replanning.

import json
from sqlalchemy.orm import Session
from app.db.models import Disruption, Event, Parcel, RouteDecision
from app.engines.routing_engine import select_next_hop
from app.utils.time_utils import utc_now_iso


def get_latest_route_for_parcel(db: Session, parcel_id: str) -> list[str]:
    decision = (
        db.query(RouteDecision)
        .filter(RouteDecision.parcel_id == parcel_id)
        .order_by(RouteDecision.id.desc())
        .first()
    )
    if decision is not None and decision.full_route:
        try:
            return json.loads(decision.full_route)
        except json.JSONDecodeError:
            pass
    parcel = db.get(Parcel, parcel_id)
    if parcel is None:
        return []
    res = select_next_hop(db, parcel_id, parcel.current_hub, parcel.destination_hub)
    return res["full_route"]


def log_disruption(
    db: Session,
    disruption_type: str,
    target_id: str,
    severity: str,
    reason: str,
) -> Disruption:
    disruption = Disruption(
        disruption_type=disruption_type,
        target_id=target_id,
        severity=severity,
        status="active",
        reason=reason,
        created_at=utc_now_iso(),
        resolved_at=None,
    )
    db.add(disruption)
    db.commit()
    db.refresh(disruption)
    return disruption


def save_agentops_event(
    db: Session,
    event_type: str,
    parcel_id: str | None,
    hub_id: str | None,
    decision: str | None,
    action: str | None,
    severity: str | None,
    reason: str | None,
    raw_payload: str | None = None,
) -> Event:
    event = Event(
        event_type=event_type,
        parcel_id=parcel_id,
        hub_id=hub_id,
        timestamp=utc_now_iso(),
        decision=decision,
        action=action,
        severity=severity,
        reason=reason,
        raw_payload=raw_payload,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def reroute_parcel(db: Session, parcel_id: str, trigger_reason: str) -> dict:
    parcel = db.get(Parcel, parcel_id)
    if parcel is None:
        raise ValueError("Parcel not found")
    result = select_next_hop(db, parcel_id, parcel.current_hub, parcel.destination_hub)
    return result
