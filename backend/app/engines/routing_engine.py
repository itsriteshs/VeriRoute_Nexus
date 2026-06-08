# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: PacketFlow next-hop scoring and route decision persistence.

import json

from sqlalchemy.orm import Session

from app.db.models import Edge, Hub, Parcel, RouteDecision
from app.engines.explanation_engine import generate_route_reason
from app.engines.graph_engine import (
    HIGH_ETA,
    find_route_via_candidate,
    get_active_edge,
    get_neighbors,
)
from app.utils.time_utils import utc_now_iso

SLA_WEIGHT = 0.30
CONGESTION_WEIGHT = 0.25
TRUST_WEIGHT = 0.20
CONDITION_WEIGHT = 0.15
COST_WEIGHT = 0.10

SENSITIVE_PARCEL_TYPES = {"medicine", "vaccine", "food", "dairy", "seafood", "cold_chain"}


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def calculate_sla_risk(total_eta_min: float, sla_minutes: int) -> float:
    if not sla_minutes or sla_minutes <= 0:
        return 0.5
    ratio = total_eta_min / sla_minutes
    if ratio <= 0.60:
        return 0.15
    if ratio <= 0.80:
        return 0.30
    if ratio <= 1.00:
        return 0.55
    if ratio <= 1.20:
        return 0.75
    return 1.00


def calculate_congestion_risk(candidate_hub: Hub) -> float:
    return clamp(candidate_hub.congestion)


def calculate_trust_risk(candidate_hub: Hub) -> float:
    return clamp(1 - candidate_hub.trust_score)


def calculate_condition_risk(db: Session, parcel: Parcel, route: list[str]) -> float:
    if parcel.parcel_type not in SENSITIVE_PARCEL_TYPES:
        return 0.20
    if parcel.temperature_limit is None:
        return 0.20

    route_after_current = route[1:]
    contains_cold_chain = any((hub := db.get(Hub, hub_id)) is not None and hub.cold_chain for hub_id in route_after_current)

    if parcel.current_temperature is None:
        return 0.35
    if parcel.current_temperature <= parcel.temperature_limit:
        return 0.10 if contains_cold_chain else 0.35
    return 0.20 if contains_cold_chain else 0.90


def calculate_cost_emission_score(edge: Edge) -> float:
    return clamp((float(edge.cost_score) + float(edge.emission_score)) / 2)


def score_candidate(
    db: Session,
    parcel: Parcel,
    current_hub: str,
    candidate_hub: Hub,
    destination_hub: str,
) -> dict[str, object]:
    route, total_eta = find_route_via_candidate(db, current_hub, candidate_hub.id, destination_hub)
    if not route or total_eta >= HIGH_ETA:
        return {
            "hub_id": candidate_hub.id,
            "full_route": [],
            "total_eta_min": HIGH_ETA,
            "sla_risk": 1.0,
            "congestion_risk": calculate_congestion_risk(candidate_hub),
            "trust_risk": calculate_trust_risk(candidate_hub),
            "condition_risk": 1.0,
            "cost_emission_score": 1.0,
            "final_score": 1.0,
            "selected": False,
            "rejection_reason": "No valid route from candidate to destination.",
        }

    edge = get_active_edge(db, current_hub, candidate_hub.id)
    if edge is None:
        raise ValueError("No active edge to candidate hub")

    sla_risk = calculate_sla_risk(total_eta, parcel.sla_minutes)
    congestion_risk = calculate_congestion_risk(candidate_hub)
    trust_risk = calculate_trust_risk(candidate_hub)
    condition_risk = calculate_condition_risk(db, parcel, route)
    cost_emission_score = calculate_cost_emission_score(edge)
    final_score = (
        SLA_WEIGHT * sla_risk
        + CONGESTION_WEIGHT * congestion_risk
        + TRUST_WEIGHT * trust_risk
        + CONDITION_WEIGHT * condition_risk
        + COST_WEIGHT * cost_emission_score
    )

    return {
        "hub_id": candidate_hub.id,
        "full_route": route,
        "total_eta_min": total_eta,
        "sla_risk": clamp(sla_risk),
        "congestion_risk": congestion_risk,
        "trust_risk": trust_risk,
        "condition_risk": clamp(condition_risk),
        "cost_emission_score": cost_emission_score,
        "final_score": clamp(final_score),
        "selected": False,
        "rejection_reason": None,
    }


def _save_route_decision(
    db: Session,
    parcel_id: str,
    current_hub: str,
    selected_next_hop: str | None,
    full_route: list[str],
    candidate_scores: list[dict[str, object]],
    final_score: float | None,
    reason: str,
) -> None:
    db.add(
        RouteDecision(
            parcel_id=parcel_id,
            current_hub=current_hub,
            selected_next_hop=selected_next_hop,
            full_route=json.dumps(full_route),
            candidate_scores=json.dumps(candidate_scores),
            final_score=final_score,
            reason=reason,
            created_at=utc_now_iso(),
        )
    )
    db.commit()


def select_next_hop(
    db: Session,
    parcel_id: str,
    current_hub: str | None = None,
    destination_hub: str | None = None,
) -> dict[str, object]:
    parcel = db.get(Parcel, parcel_id)
    if parcel is None:
        raise ValueError("Parcel not found")

    resolved_current_hub = current_hub or parcel.current_hub
    resolved_destination_hub = destination_hub or parcel.destination_hub

    if db.get(Hub, resolved_current_hub) is None:
        raise ValueError("Current hub not found")
    if db.get(Hub, resolved_destination_hub) is None:
        raise ValueError("Destination hub not found")

    candidate_scores = [
        score_candidate(db, parcel, resolved_current_hub, candidate_hub, resolved_destination_hub)
        for candidate_hub in get_neighbors(db, resolved_current_hub)
    ]
    valid_scores = [candidate for candidate in candidate_scores if candidate["rejection_reason"] is None]

    if not valid_scores:
        reason = "No valid route available from current hub to destination."
        _save_route_decision(db, parcel.id, resolved_current_hub, None, [], [], None, reason)
        return {
            "parcel_id": parcel.id,
            "current_hub": resolved_current_hub,
            "destination_hub": resolved_destination_hub,
            "selected_next_hop": None,
            "full_route": [],
            "total_eta_min": 0.0,
            "final_score": 1.0,
            "candidate_scores": [],
            "reason": reason,
        }

    selected = min(valid_scores, key=lambda candidate: (float(candidate["final_score"]), float(candidate["total_eta_min"]), str(candidate["hub_id"])))
    for candidate in candidate_scores:
        candidate["selected"] = candidate["hub_id"] == selected["hub_id"]

    reason = generate_route_reason(parcel, selected, candidate_scores)
    _save_route_decision(
        db,
        parcel.id,
        resolved_current_hub,
        str(selected["hub_id"]),
        selected["full_route"],  # type: ignore[arg-type]
        candidate_scores,
        float(selected["final_score"]),
        reason,
    )

    return {
        "parcel_id": parcel.id,
        "current_hub": resolved_current_hub,
        "destination_hub": resolved_destination_hub,
        "selected_next_hop": selected["hub_id"],
        "full_route": selected["full_route"],
        "total_eta_min": selected["total_eta_min"],
        "final_score": selected["final_score"],
        "candidate_scores": candidate_scores,
        "reason": reason,
    }
