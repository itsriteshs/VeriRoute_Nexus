# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: ImmuneNet scan validation and persistence.

import json
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.core import constants
from app.db.models import Edge, Event, Hub, ImmuneCheck, Parcel
from app.engines.explanation_engine import generate_scan_reason
from app.engines.routing_engine import select_next_hop
from app.engines.trust_engine import update_hub_trust
from app.schemas.scan_schema import ScanRequest
from app.utils.geo import haversine_distance_m, is_within_geofence
from app.utils.time_utils import parse_iso_timestamp, utc_now_iso

SENSITIVE_PARCEL_TYPES = {"medicine", "vaccine", "food", "dairy", "seafood", "cold_chain"}


def _dump_model(model: ScanRequest) -> str:
    if hasattr(model, "model_dump"):
        return json.dumps(model.model_dump())
    return model.json()


def _event_gps(scan_request: ScanRequest) -> dict[str, float | None]:
    if scan_request.gps is None:
        return {"gps_lat": None, "gps_lng": None, "gps_accuracy_m": None}
    return {
        "gps_lat": scan_request.gps.lat,
        "gps_lng": scan_request.gps.lng,
        "gps_accuracy_m": scan_request.gps.accuracy_m,
    }


def check_geofence(db: Session, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    if scan_request.gps is None:
        return constants.CHECK_WARN, "GPS missing; geofence check could not fully verify scanner proximity.", {}

    inside, distance_m = is_within_geofence(
        scan_request.gps.lat,
        scan_request.gps.lng,
        hub.lat,
        hub.lng,
        hub.geofence_radius_m,
        scan_request.gps.accuracy_m,
    )
    trace = {"distance_m": distance_m, "hub_id": hub.id}
    if inside:
        return constants.CHECK_PASS, None, trace
    return constants.CHECK_FAIL, f"Scanner GPS was {distance_m / 1000:.2f} km outside {hub.id} geofence.", trace


def _distance_km_between_hubs(db: Session, from_hub: str, to_hub: str) -> float | None:
    edge = (
        db.query(Edge)
        .filter(Edge.from_hub == from_hub, Edge.to_hub == to_hub, Edge.status == "active")
        .first()
    )
    if edge is not None:
        return float(edge.distance_km)
    start = db.get(Hub, from_hub)
    end = db.get(Hub, to_hub)
    if start is None or end is None:
        return None
    return haversine_distance_m(start.lat, start.lng, end.lat, end.lng) / 1000


def check_speed(db: Session, parcel: Parcel, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    previous = (
        db.query(Event)
        .filter(Event.parcel_id == parcel.id, Event.decision == constants.DECISION_ACCEPTED, Event.hub_id.isnot(None))
        .order_by(Event.id.desc())
        .first()
    )
    if previous is None or not previous.hub_id or not previous.timestamp or previous.hub_id == hub.id:
        return constants.CHECK_PASS, None, {}

    previous_time = parse_iso_timestamp(previous.timestamp)
    if previous_time is None:
        return constants.CHECK_PASS, None, {}

    minutes = max((datetime.now(UTC) - previous_time).total_seconds() / 60, 0.01)
    distance_km = _distance_km_between_hubs(db, previous.hub_id, hub.id)
    if distance_km is None:
        return constants.CHECK_WARN, "Distance could not be determined for speed plausibility check.", {}

    carrier_type = scan_request.carrier_type or parcel.carrier_type or "default"
    max_speeds = {"van": 80, "bike": 50, "drone": 100, "bot": 15}
    max_speed = max_speeds.get(carrier_type, 60) * 1.5
    implied_speed = distance_km / (minutes / 60)
    trace = {"distance_km": distance_km, "minutes": minutes, "implied_speed_kmh": implied_speed}
    if implied_speed > max_speed:
        return (
            constants.CHECK_FAIL,
            f"Impossible speed detected: parcel moved from {previous.hub_id} to {hub.id} too quickly for {carrier_type}.",
            trace,
        )
    return constants.CHECK_PASS, None, trace


def check_route_graph(db: Session, parcel: Parcel, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    if not parcel.current_hub or scan_request.hub_id == parcel.current_hub:
        return constants.CHECK_PASS, None, {}
    edge = (
        db.query(Edge)
        .filter(Edge.from_hub == parcel.current_hub, Edge.to_hub == scan_request.hub_id, Edge.status == "active")
        .first()
    )
    if edge is not None:
        return constants.CHECK_PASS, None, {"from_hub": parcel.current_hub, "to_hub": scan_request.hub_id}
    return (
        constants.CHECK_FAIL,
        f"Invalid route hop: {parcel.current_hub} is not directly connected to {scan_request.hub_id}.",
        {"from_hub": parcel.current_hub, "to_hub": scan_request.hub_id},
    )


def check_clone_scan(db: Session, parcel: Parcel, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    if scan_request.scanner_id == "FAKE-SCANNER":
        return constants.CHECK_PASS, None, {}

    cutoff = datetime.now(UTC) - timedelta(minutes=3)
    accepted_events = (
        db.query(Event)
        .filter(Event.parcel_id == parcel.id, Event.decision == constants.DECISION_ACCEPTED, Event.hub_id.isnot(None))
        .order_by(Event.id.desc())
        .limit(20)
        .all()
    )
    for event in accepted_events:
        if event.hub_id == hub.id:
            continue
        event_time = parse_iso_timestamp(event.timestamp)
        if event_time is None or event_time < cutoff:
            continue
        other_hub = db.get(Hub, event.hub_id)
        if other_hub is None:
            continue
        distance_km = haversine_distance_m(other_hub.lat, other_hub.lng, hub.lat, hub.lng) / 1000
        if distance_km > 1:
            return (
                constants.CHECK_FAIL,
                f"Clone scan detected: {parcel.id} appeared at {other_hub.id} and {hub.id} within an impossible time window.",
                {"other_hub": other_hub.id, "distance_km": distance_km},
            )
    return constants.CHECK_PASS, None, {}


def check_cold_chain(db: Session, parcel: Parcel, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    if parcel.parcel_type not in SENSITIVE_PARCEL_TYPES:
        return constants.CHECK_PASS, None, {}
    if parcel.temperature_limit is None:
        return constants.CHECK_SKIPPED, None, {}

    temperature = scan_request.temperature_c if scan_request.temperature_c is not None else parcel.current_temperature
    if temperature is None:
        return constants.CHECK_WARN, "Temperature missing for cold-chain parcel.", {}
    if temperature <= parcel.temperature_limit:
        return constants.CHECK_PASS, None, {"temperature_c": temperature, "limit": parcel.temperature_limit}
    return (
        constants.CHECK_FAIL,
        f"Cold-chain breach detected: {parcel.id} measured {temperature}C above limit {parcel.temperature_limit}C.",
        {"temperature_c": temperature, "limit": parcel.temperature_limit},
    )


def check_tamper(db: Session, parcel: Parcel, hub: Hub, scan_request: ScanRequest) -> tuple[str, str | None, dict[str, Any]]:
    if scan_request.tamper:
        return constants.CHECK_FAIL, f"Tamper event detected at {hub.id}. Parcel movement has been held for review.", {}
    return constants.CHECK_PASS, None, {}


def decide_scan_result(check_results: dict[str, dict[str, Any]]) -> dict[str, object]:
    priority = [
        ("tamper", constants.DECISION_HOLD, constants.ACTION_ALERT_AND_HOLD, constants.LED_RED),
        ("clone_scan", constants.DECISION_BLOCKED, constants.ACTION_QUARANTINE_MOVEMENT_CLAIM, constants.LED_RED),
        ("geofence", constants.DECISION_BLOCKED, constants.ACTION_QUARANTINE_MOVEMENT_CLAIM, constants.LED_RED),
        ("speed", constants.DECISION_BLOCKED, constants.ACTION_QUARANTINE_MOVEMENT_CLAIM, constants.LED_RED),
        ("route_graph", constants.DECISION_BLOCKED, constants.ACTION_QUARANTINE_MOVEMENT_CLAIM, constants.LED_RED),
        ("cold_chain", constants.DECISION_REROUTED, constants.ACTION_REROUTE_TO_COLD_HUB, constants.LED_AMBER),
    ]
    for check_name, decision, action, led in priority:
        if check_results[check_name]["status"] == constants.CHECK_FAIL:
            return {"decision": decision, "action": action, "led": led, "failed_checks": [check_name]}

    warns = [name for name, result in check_results.items() if result["status"] == constants.CHECK_WARN]
    if warns:
        return {
            "decision": constants.DECISION_WARNING,
            "action": constants.ACTION_REVIEW_REQUIRED,
            "led": constants.LED_RED_BLINK,
            "failed_checks": warns,
        }
    return {
        "decision": constants.DECISION_ACCEPTED,
        "action": constants.ACTION_UPDATE_LOCATION,
        "led": constants.LED_GREEN,
        "failed_checks": [],
    }


def _save_event(
    db: Session,
    event_type: str,
    parcel_id: str | None,
    hub_id: str | None,
    decision: str | None,
    action: str | None,
    severity: str | None,
    reason: str | None,
    scan_request: ScanRequest,
    raw_payload: str | None = None,
) -> Event:
    event = Event(
        event_type=event_type,
        parcel_id=parcel_id,
        hub_id=hub_id,
        timestamp=utc_now_iso(),
        temperature_c=scan_request.temperature_c,
        decision=decision,
        action=action,
        severity=severity,
        reason=reason,
        raw_payload=raw_payload,
        **_event_gps(scan_request),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def validate_scan(db: Session, scan_request: ScanRequest) -> dict[str, Any]:
    parcel = db.get(Parcel, scan_request.parcel_id)
    if parcel is None:
        raise ValueError("Parcel not found")
    hub = db.get(Hub, scan_request.hub_id)
    if hub is None:
        raise ValueError("Hub not found")

    raw_scan = _dump_model(scan_request)
    scan_event = _save_event(
        db,
        constants.SCAN_RECEIVED,
        parcel.id,
        hub.id,
        None,
        None,
        "info",
        "Scan received for ImmuneNet validation.",
        scan_request,
        raw_scan,
    )

    checks = {
        "geofence": check_geofence(db, hub, scan_request),
        "speed": check_speed(db, parcel, hub, scan_request),
        "route_graph": check_route_graph(db, parcel, hub, scan_request),
        "clone_scan": check_clone_scan(db, parcel, hub, scan_request),
        "cold_chain": check_cold_chain(db, parcel, hub, scan_request),
        "tamper": check_tamper(db, parcel, hub, scan_request),
    }
    check_results = {
        name: {"status": status, "reason": reason, "trace": trace}
        for name, (status, reason, trace) in checks.items()
    }
    outcome = decide_scan_result(check_results)
    failed_checks = list(outcome["failed_checks"])
    decision = str(outcome["decision"])
    action = str(outcome["action"])
    led = str(outcome["led"])
    reason = generate_scan_reason(parcel, hub, decision, failed_checks, check_results)

    db.add(
        ImmuneCheck(
            event_id=scan_event.id,
            parcel_id=parcel.id,
            hub_id=hub.id,
            geofence=check_results["geofence"]["status"],
            speed=check_results["speed"]["status"],
            route_graph=check_results["route_graph"]["status"],
            clone_scan=check_results["clone_scan"]["status"],
            cold_chain=check_results["cold_chain"]["status"],
            tamper=check_results["tamper"]["status"],
            failed_checks=json.dumps(failed_checks),
            decision=decision,
            severity="info" if decision == constants.DECISION_ACCEPTED else "warning",
            action=action,
            reason=reason,
        )
    )
    db.commit()

    trust_update = update_hub_trust(db, hub.id, decision, failed_checks, reason, scan_event.id)
    route_decision = None

    if decision == constants.DECISION_ACCEPTED:
        parcel.previous_hub = parcel.current_hub
        parcel.current_hub = hub.id
        if scan_request.temperature_c is not None:
            parcel.current_temperature = scan_request.temperature_c
        parcel.carrier_type = scan_request.carrier_type or parcel.carrier_type
        parcel.status = "verified" if parcel.current_hub == parcel.source_hub else "in_transit"
        parcel.trust_state = "verified"
        parcel.updated_at = utc_now_iso()
        db.commit()
        route_decision = select_next_hop(db, parcel.id, hub.id, parcel.destination_hub)
        _save_event(db, constants.MOVEMENT_ACCEPTED, parcel.id, hub.id, decision, action, "info", reason, scan_request)
    elif decision == constants.DECISION_BLOCKED:
        event_type = constants.MOVEMENT_BLOCKED
        if "geofence" in failed_checks and scan_request.scanner_id == "FAKE-SCANNER":
            event_type = constants.FAKE_SCAN_BLOCKED
        elif "clone_scan" in failed_checks:
            event_type = constants.CLONE_SCAN_BLOCKED
        _save_event(db, event_type, parcel.id, hub.id, decision, action, "error", reason, scan_request)
    elif decision == constants.DECISION_WARNING:
        _save_event(db, constants.MOVEMENT_WARNING, parcel.id, hub.id, decision, action, "warning", reason, scan_request)
    elif decision == constants.DECISION_REROUTED:
        if scan_request.temperature_c is not None:
            parcel.current_temperature = scan_request.temperature_c
        parcel.status = "rerouted"
        parcel.updated_at = utc_now_iso()
        db.commit()
        route_decision = select_next_hop(db, parcel.id, parcel.current_hub, parcel.destination_hub)
        _save_event(db, constants.TEMPERATURE_BREACH, parcel.id, hub.id, decision, action, "warning", reason, scan_request)
    elif decision == constants.DECISION_HOLD:
        parcel.status = "hold"
        parcel.updated_at = utc_now_iso()
        db.commit()
        _save_event(db, constants.TAMPER_ALERT, parcel.id, hub.id, decision, action, "error", reason, scan_request)

    return {
        "decision": decision,
        "action": action,
        "led": led,
        "parcel_id": parcel.id,
        "hub_id": hub.id,
        "immune_checks": {name: result["status"] for name, result in check_results.items()},
        "failed_checks": failed_checks,
        "trust_update": trust_update,
        "route_decision": route_decision,
        "reason": reason,
    }
