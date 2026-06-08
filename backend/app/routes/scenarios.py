# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: scenario and disruption API routes.

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import constants
from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Hub, Edge, Parcel, RouteDecision
from app.engines.graph_engine import find_shortest_route_by_eta
from app.engines.agentops_engine import (
    get_latest_route_for_parcel,
    log_disruption,
    save_agentops_event,
)
from app.engines.routing_engine import select_next_hop
from app.engines.explanation_engine import generate_agentops_reason
from app.engines.metrics_engine import get_starter_metrics
from app.utils.time_utils import utc_now_iso
from app.schemas.scenario_schema import (
    FailHubRequest,
    OverloadHubRequest,
    TrafficJamRequest,
    WeatherRiskRequest,
    TempBreachRequest,
    ScenarioResponse,
)

router = APIRouter(prefix="/scenario", tags=["scenarios"])


def _find_cold_chain_route(db: Session, start_hub: str, destination_hub: str) -> list[str]:
    cold_hubs = (
        db.query(Hub)
        .filter(Hub.cold_chain == True, Hub.status != "failed", Hub.trust_score >= 0.40)  # noqa: E712
        .order_by(Hub.id)
        .all()
    )
    best_route: list[str] = []
    best_eta = float("inf")
    for cold_hub in cold_hubs:
        first_leg, first_eta = find_shortest_route_by_eta(db, start_hub, cold_hub.id)
        second_leg, second_eta = find_shortest_route_by_eta(db, cold_hub.id, destination_hub)
        if not first_leg or not second_leg:
            continue
        route = [*first_leg, *second_leg[1:]]
        eta = first_eta + second_eta
        dedicated_penalty = 0.0 if "COLD" in cold_hub.id else 10_000.0
        score = eta + dedicated_penalty
        if route and cold_hub.id in route and score < best_eta:
            best_route = route
            best_eta = float(score)
    return best_route


def _save_forced_route_decision(
    db: Session,
    parcel_id: str,
    current_hub: str,
    full_route: list[str],
    reason: str,
) -> None:
    db.add(
        RouteDecision(
            parcel_id=parcel_id,
            current_hub=current_hub,
            selected_next_hop=full_route[1] if len(full_route) > 1 else None,
            full_route=json.dumps(full_route),
            candidate_scores=json.dumps([]),
            final_score=None,
            reason=reason,
            created_at=utc_now_iso(),
        )
    )
    db.commit()


@router.post("/fail-hub", response_model=ScenarioResponse)
async def fail_hub(payload: FailHubRequest, db: Session = Depends(get_db)):
    hub = db.get(Hub, payload.hub_id)
    if hub is None:
        raise HTTPException(status_code=404, detail="Hub not found")

    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    old_route = get_latest_route_for_parcel(db, payload.parcel_id)

    hub.status = "failed"
    hub.congestion = 1.0
    db.commit()

    log_disruption(
        db,
        disruption_type="hub_failed",
        target_id=payload.hub_id,
        severity="high",
        reason=f"Hub {payload.hub_id} failed.",
    )

    save_agentops_event(
        db,
        event_type=constants.HUB_FAILED,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="DISRUPTION",
        action="REPLAN_ROUTE",
        severity="error",
        reason=f"Hub {payload.hub_id} failed.",
    )

    new_route_res = select_next_hop(db, payload.parcel_id, parcel.current_hub, parcel.destination_hub)
    new_route = new_route_res.get("full_route") or []

    await safe_broadcast(constants.HUB_FAILED, {"hub_id": payload.hub_id, "status": "failed"})

    if not new_route:
        reason = "No valid route available after disruption."
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))
        return {
            "disruption": {"type": "hub_failed", "target": payload.hub_id},
            "agentops": {"detected": True, "action": "REPLAN_ROUTE", "status": "NO_VALID_ROUTE"},
            "old_route": old_route,
            "new_route": [],
            "reason": reason,
        }

    reason = generate_agentops_reason("hub_failed", payload.hub_id, old_route, new_route, payload.parcel_id)

    save_agentops_event(
        db,
        event_type=constants.REROUTE_TRIGGERED,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="REROUTED",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=reason,
        raw_payload=json.dumps(
            {
                "old_route": old_route,
                "new_route": new_route,
                "trigger": "hub_failed",
                "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
            }
        ),
    )

    await safe_broadcast(
        constants.REROUTE_TRIGGERED,
        {"parcel_id": payload.parcel_id, "old_route": old_route, "new_route": new_route, "trigger": "hub_failed"},
    )

    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": new_route_res["parcel_id"],
            "current_hub": new_route_res["current_hub"],
            "selected_next_hop": new_route_res["selected_next_hop"],
            "full_route": new_route_res["full_route"],
            "candidate_scores": new_route_res["candidate_scores"],
            "reason": new_route_res["reason"],
        },
    )

    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return {
        "disruption": {"type": "hub_failed", "target": payload.hub_id},
        "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
        "old_route": old_route,
        "new_route": new_route,
        "reason": reason,
    }


@router.post("/overload-hub", response_model=ScenarioResponse)
async def overload_hub(payload: OverloadHubRequest, db: Session = Depends(get_db)):
    hub = db.get(Hub, payload.hub_id)
    if hub is None:
        raise HTTPException(status_code=404, detail="Hub not found")

    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    old_route = get_latest_route_for_parcel(db, payload.parcel_id)

    hub.status = "overloaded"
    hub.congestion = payload.congestion
    db.commit()

    log_disruption(
        db,
        disruption_type="hub_overloaded",
        target_id=payload.hub_id,
        severity="medium",
        reason=f"Hub {payload.hub_id} overloaded with congestion {payload.congestion}.",
    )

    save_agentops_event(
        db,
        event_type=constants.HUB_OVERLOADED,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="DISRUPTION",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=f"Hub {payload.hub_id} is overloaded with congestion {payload.congestion}.",
    )

    new_route_res = select_next_hop(db, payload.parcel_id, parcel.current_hub, parcel.destination_hub)
    new_route = new_route_res.get("full_route") or []

    await safe_broadcast(
        constants.HUB_OVERLOADED, {"hub_id": payload.hub_id, "status": "overloaded", "congestion": payload.congestion}
    )

    if not new_route:
        reason = "No valid route available after disruption."
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))
        return {
            "disruption": {"type": "hub_overloaded", "target": payload.hub_id},
            "agentops": {"detected": True, "action": "REPLAN_ROUTE", "status": "NO_VALID_ROUTE"},
            "old_route": old_route,
            "new_route": [],
            "reason": reason,
        }

    reason = generate_agentops_reason("hub_overloaded", payload.hub_id, old_route, new_route, payload.parcel_id)

    save_agentops_event(
        db,
        event_type=constants.REROUTE_TRIGGERED,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="REROUTED",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=reason,
        raw_payload=json.dumps(
            {
                "old_route": old_route,
                "new_route": new_route,
                "trigger": "hub_overloaded",
                "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
            }
        ),
    )

    await safe_broadcast(
        constants.REROUTE_TRIGGERED,
        {"parcel_id": payload.parcel_id, "old_route": old_route, "new_route": new_route, "trigger": "hub_overloaded"},
    )

    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": new_route_res["parcel_id"],
            "current_hub": new_route_res["current_hub"],
            "selected_next_hop": new_route_res["selected_next_hop"],
            "full_route": new_route_res["full_route"],
            "candidate_scores": new_route_res["candidate_scores"],
            "reason": new_route_res["reason"],
        },
    )

    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return {
        "disruption": {"type": "hub_overloaded", "target": payload.hub_id},
        "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
        "old_route": old_route,
        "new_route": new_route,
        "reason": reason,
    }


@router.post("/traffic-jam", response_model=ScenarioResponse)
async def traffic_jam(payload: TrafficJamRequest, db: Session = Depends(get_db)):
    edge = db.query(Edge).filter(Edge.from_hub == payload.from_hub, Edge.to_hub == payload.to_hub).first()
    if edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")

    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    old_route = get_latest_route_for_parcel(db, payload.parcel_id)

    edge.traffic_risk = payload.traffic_risk
    edge.eta_min += 10.0
    db.commit()

    target_id = f"{payload.from_hub}->{payload.to_hub}"

    log_disruption(
        db,
        disruption_type="traffic_jam",
        target_id=target_id,
        severity="medium",
        reason=f"Traffic jam between {payload.from_hub} and {payload.to_hub}.",
    )

    save_agentops_event(
        db,
        event_type=constants.TRAFFIC_JAM,
        parcel_id=payload.parcel_id,
        hub_id=payload.from_hub,
        decision="DISRUPTION",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=f"Traffic jam detected on route segment {target_id}.",
    )

    new_route_res = select_next_hop(db, payload.parcel_id, parcel.current_hub, parcel.destination_hub)
    new_route = new_route_res.get("full_route") or []

    await safe_broadcast(
        constants.TRAFFIC_JAM,
        {"from_hub": payload.from_hub, "to_hub": payload.to_hub, "traffic_risk": payload.traffic_risk},
    )

    if not new_route:
        reason = "No valid route available after disruption."
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))
        return {
            "disruption": {"type": "traffic_jam", "target": target_id},
            "agentops": {"detected": True, "action": "REPLAN_ROUTE", "status": "NO_VALID_ROUTE"},
            "old_route": old_route,
            "new_route": [],
            "reason": reason,
        }

    reason = generate_agentops_reason("traffic_jam", target_id, old_route, new_route, payload.parcel_id)

    save_agentops_event(
        db,
        event_type=constants.REROUTE_TRIGGERED,
        parcel_id=payload.parcel_id,
        hub_id=payload.from_hub,
        decision="REROUTED",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=reason,
        raw_payload=json.dumps(
            {
                "old_route": old_route,
                "new_route": new_route,
                "trigger": "traffic_jam",
                "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
            }
        ),
    )

    await safe_broadcast(
        constants.REROUTE_TRIGGERED,
        {"parcel_id": payload.parcel_id, "old_route": old_route, "new_route": new_route, "trigger": "traffic_jam"},
    )

    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": new_route_res["parcel_id"],
            "current_hub": new_route_res["current_hub"],
            "selected_next_hop": new_route_res["selected_next_hop"],
            "full_route": new_route_res["full_route"],
            "candidate_scores": new_route_res["candidate_scores"],
            "reason": new_route_res["reason"],
        },
    )

    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return {
        "disruption": {"type": "traffic_jam", "target": target_id},
        "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
        "old_route": old_route,
        "new_route": new_route,
        "reason": reason,
    }


@router.post("/weather-risk", response_model=ScenarioResponse)
async def weather_risk(payload: WeatherRiskRequest, db: Session = Depends(get_db)):
    edge = db.query(Edge).filter(Edge.from_hub == payload.from_hub, Edge.to_hub == payload.to_hub).first()
    if edge is None:
        raise HTTPException(status_code=404, detail="Edge not found")

    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    old_route = get_latest_route_for_parcel(db, payload.parcel_id)

    edge.weather_risk = payload.weather_risk
    edge.eta_min += 12.0
    db.commit()

    target_id = f"{payload.from_hub}->{payload.to_hub}"

    log_disruption(
        db,
        disruption_type="weather_risk",
        target_id=target_id,
        severity="medium",
        reason=f"Weather risk between {payload.from_hub} and {payload.to_hub}.",
    )

    save_agentops_event(
        db,
        event_type=constants.WEATHER_RISK,
        parcel_id=payload.parcel_id,
        hub_id=payload.from_hub,
        decision="DISRUPTION",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=f"Weather risk detected on route segment {target_id}.",
    )

    new_route_res = select_next_hop(db, payload.parcel_id, parcel.current_hub, parcel.destination_hub)
    new_route = new_route_res.get("full_route") or []

    await safe_broadcast(
        constants.WEATHER_RISK,
        {"from_hub": payload.from_hub, "to_hub": payload.to_hub, "weather_risk": payload.weather_risk},
    )

    if not new_route:
        reason = "No valid route available after disruption."
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))
        return {
            "disruption": {"type": "weather_risk", "target": target_id},
            "agentops": {"detected": True, "action": "REPLAN_ROUTE", "status": "NO_VALID_ROUTE"},
            "old_route": old_route,
            "new_route": [],
            "reason": reason,
        }

    reason = generate_agentops_reason("weather_risk", target_id, old_route, new_route, payload.parcel_id)

    save_agentops_event(
        db,
        event_type=constants.REROUTE_TRIGGERED,
        parcel_id=payload.parcel_id,
        hub_id=payload.from_hub,
        decision="REROUTED",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=reason,
        raw_payload=json.dumps(
            {
                "old_route": old_route,
                "new_route": new_route,
                "trigger": "weather_risk",
                "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
            }
        ),
    )

    await safe_broadcast(
        constants.REROUTE_TRIGGERED,
        {"parcel_id": payload.parcel_id, "old_route": old_route, "new_route": new_route, "trigger": "weather_risk"},
    )

    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": new_route_res["parcel_id"],
            "current_hub": new_route_res["current_hub"],
            "selected_next_hop": new_route_res["selected_next_hop"],
            "full_route": new_route_res["full_route"],
            "candidate_scores": new_route_res["candidate_scores"],
            "reason": new_route_res["reason"],
        },
    )

    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return {
        "disruption": {"type": "weather_risk", "target": target_id},
        "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
        "old_route": old_route,
        "new_route": new_route,
        "reason": reason,
    }


@router.post("/temp-breach")
async def temp_breach(payload: TempBreachRequest, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, payload.parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    old_route = get_latest_route_for_parcel(db, payload.parcel_id)

    parcel.current_temperature = payload.temperature_c
    parcel.status = "rerouted"
    db.commit()

    log_disruption(
        db,
        disruption_type="temperature_breach",
        target_id=payload.parcel_id,
        severity="high",
        reason=f"Temperature breach: {payload.temperature_c}C",
    )

    save_agentops_event(
        db,
        event_type=constants.TEMPERATURE_BREACH,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="REROUTED",
        action="REROUTE_TO_COLD_HUB",
        severity="error",
        reason=f"Cold-chain risk detected. {payload.parcel_id} exceeded {parcel.temperature_limit}C.",
    )

    route_origin = parcel.current_hub
    if not db.get(Hub, route_origin) or db.get(Hub, route_origin).status == "failed":
        route_origin = payload.hub_id

    cold_route = _find_cold_chain_route(db, route_origin, parcel.destination_hub)
    if cold_route:
        new_route = cold_route
        selected_next_hop = cold_route[1] if len(cold_route) > 1 else None
        forced_reason = f"Cold-chain risk detected. {payload.parcel_id} exceeded {parcel.temperature_limit}C, so PacketFlow forced a route through COLD-HUB-C."
        _save_forced_route_decision(db, payload.parcel_id, route_origin, new_route, forced_reason)
        new_route_res = {
            "parcel_id": payload.parcel_id,
            "current_hub": route_origin,
            "selected_next_hop": selected_next_hop,
            "full_route": new_route,
            "candidate_scores": [],
            "reason": forced_reason,
        }
    else:
        new_route_res = select_next_hop(db, payload.parcel_id, route_origin, parcel.destination_hub)
        new_route = new_route_res.get("full_route") or []

    await safe_broadcast(
        constants.TEMPERATURE_BREACH,
        {
            "parcel_id": payload.parcel_id,
            "hub_id": payload.hub_id,
            "temperature_c": payload.temperature_c,
            "temperature_limit": parcel.temperature_limit,
            "decision": "REROUTED",
            "reason": f"Cold-chain risk detected. {payload.parcel_id} exceeded {parcel.temperature_limit}C.",
        },
    )

    if not new_route:
        reason = (
            "Cold-chain breach detected, but no valid cold-chain-safe route is available "
            f"from {route_origin} to {parcel.destination_hub} with current hub/edge status."
        )
        await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))
        return {
            "decision": "REROUTED",
            "action": "REROUTE_TO_COLD_HUB",
            "parcel_id": payload.parcel_id,
            "temperature_c": payload.temperature_c,
            "temperature_limit": parcel.temperature_limit,
            "cold_chain_status": "BREACH",
            "old_route": old_route,
            "new_route": [],
            "reason": reason,
        }

    if "COLD-HUB-C" in new_route:
        reason = f"Cold-chain risk detected. {payload.parcel_id} exceeded {parcel.temperature_limit}C, so PacketFlow rerouted it through COLD-HUB-C."
    else:
        reason = generate_agentops_reason("temperature_breach", payload.hub_id, old_route, new_route, payload.parcel_id)

    save_agentops_event(
        db,
        event_type=constants.REROUTE_TRIGGERED,
        parcel_id=payload.parcel_id,
        hub_id=payload.hub_id,
        decision="REROUTED",
        action="REPLAN_ROUTE",
        severity="warning",
        reason=reason,
        raw_payload=json.dumps(
            {
                "old_route": old_route,
                "new_route": new_route,
                "trigger": "temperature_breach",
                "agentops": {"detected": True, "action": "REPLAN_ROUTE"},
                "cold_chain_forced": "COLD-HUB-C" in new_route,
            }
        ),
    )

    await safe_broadcast(
        constants.REROUTE_TRIGGERED,
        {"parcel_id": payload.parcel_id, "old_route": old_route, "new_route": new_route, "trigger": "temperature_breach"},
    )

    await safe_broadcast(
        constants.ROUTE_DECISION,
        {
            "parcel_id": new_route_res["parcel_id"],
            "current_hub": new_route_res["current_hub"],
            "selected_next_hop": new_route_res["selected_next_hop"],
            "full_route": new_route_res["full_route"],
            "candidate_scores": new_route_res["candidate_scores"],
            "reason": new_route_res["reason"],
        },
    )

    await safe_broadcast(constants.METRICS_UPDATED, get_starter_metrics(db))

    return {
        "decision": "REROUTED",
        "action": "REROUTE_TO_COLD_HUB",
        "parcel_id": payload.parcel_id,
        "temperature_c": payload.temperature_c,
        "temperature_limit": parcel.temperature_limit,
        "cold_chain_status": "BREACH",
        "old_route": old_route,
        "new_route": new_route,
        "reason": reason,
    }
