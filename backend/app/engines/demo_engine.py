# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Demo engine containing reset, snapshot, and end-to-end validation utilities.

import json
from sqlalchemy.orm import Session

from app.core import constants
from app.db.models import Disruption, Hub, Edge, Parcel, Event, RouteDecision
from app.db.seed_data import seed_demo_data
from app.engines.metrics_engine import get_starter_metrics
from app.engines.trust_engine import get_trust_status
from app.routes.ledger import serialize_event
from app.routes.parcels import serialize_parcel
from app.routes.routing import serialize_route_decision


def reset_demo_state(db: Session) -> dict:
    seed_demo_data(db)
    return {
        "status": "reset_complete",
        "hubs": 7,
        "edges": 8,
        "demo_parcel": "MED-104",
        "message": "Demo state restored."
    }


def get_demo_snapshot(db: Session) -> dict:
    parcel = db.get(Parcel, "MED-104")
    parcel_dict = {}
    if parcel:
        parcel_dict = serialize_parcel(parcel)

    parcels_list = [serialize_parcel(item) for item in db.query(Parcel).order_by(Parcel.id).all()]

    hubs = db.query(Hub).order_by(Hub.id).all()
    hubs_list = [
        {
            "id": hub.id,
            "name": hub.name,
            "lat": hub.lat,
            "lng": hub.lng,
            "geofence_radius_m": hub.geofence_radius_m,
            "trust_score": hub.trust_score,
            "trust_status": get_trust_status(hub.trust_score),
            "status": hub.status,
            "congestion": hub.congestion,
            "cold_chain": hub.cold_chain,
            "anomaly_count": hub.anomaly_count,
        }
        for hub in hubs
    ]

    edges = db.query(Edge).order_by(Edge.from_hub, Edge.to_hub).all()
    edges_list = [
        {
            "id": edge.id,
            "from_hub": edge.from_hub,
            "to_hub": edge.to_hub,
            "distance_km": edge.distance_km,
            "eta_min": edge.eta_min,
            "traffic_risk": edge.traffic_risk,
            "weather_risk": edge.weather_risk,
            "cost_score": edge.cost_score,
            "emission_score": edge.emission_score,
            "allowed_carriers": edge.allowed_carriers,
            "status": edge.status,
        }
        for edge in edges
    ]

    decision = (
        db.query(RouteDecision)
        .filter(RouteDecision.parcel_id == "MED-104")
        .order_by(RouteDecision.id.desc())
        .first()
    )
    latest_route_dict = {}
    if decision is None and parcel:
        from app.engines.routing_engine import select_next_hop

        select_next_hop(db, parcel.id, parcel.current_hub, parcel.destination_hub)
        decision = (
            db.query(RouteDecision)
            .filter(RouteDecision.parcel_id == "MED-104")
            .order_by(RouteDecision.id.desc())
            .first()
        )
    if decision:
        latest_route_dict = serialize_route_decision(decision)
        latest_route_dict["current_route"] = latest_route_dict["full_route"]
        latest_route_dict["latest_reason"] = latest_route_dict["reason"]
    else:
        latest_route_dict = {
            "id": 0,
            "parcel_id": "MED-104",
            "current_hub": "HUB-A",
            "selected_next_hop": "HUB-B",
            "full_route": ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"],
            "candidate_scores": [],
            "final_score": 0.27,
            "reason": "Central Smart Hub A initialized with active next-hop relay routing to HUB-B.",
            "created_at": utc_now_iso(),
            "current_route": ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"],
            "latest_reason": "Central Smart Hub A initialized with active next-hop relay routing to HUB-B."
        }

    trust_board_list = [
        {
            "hub_id": hub.id,
            "name": hub.name,
            "trust_score": hub.trust_score,
            "trust_status": get_trust_status(hub.trust_score),
        }
        for hub in hubs
    ]

    metrics = get_starter_metrics(db)

    recent_events = (
        db.query(Event)
        .order_by(Event.id.desc())
        .limit(20)
        .all()
    )
    events_list = [serialize_event(e) for e in recent_events]

    disruptions = (
        db.query(Disruption)
        .order_by(Disruption.id.desc())
        .limit(20)
        .all()
    )
    disruptions_list = [
        {
            "id": disruption.id,
            "disruption_type": disruption.disruption_type,
            "target_id": disruption.target_id,
            "severity": disruption.severity,
            "status": disruption.status,
            "reason": disruption.reason,
            "created_at": disruption.created_at,
            "resolved_at": disruption.resolved_at,
        }
        for disruption in disruptions
    ]

    return {
        "parcel": parcel_dict,
        "parcels": parcels_list,
        "hubs": hubs_list,
        "edges": edges_list,
        "latest_route": latest_route_dict,
        "trust_board": trust_board_list,
        "metrics": metrics,
        "latest_events": events_list,
        "recent_events": events_list,
        "active_disruptions": disruptions_list,
    }


async def validate_demo_flow(db: Session) -> dict:
    from app.engines.routing_engine import select_next_hop
    from app.routes.scan import process_and_broadcast_scan
    from app.schemas.scan_schema import ScanRequest

    checks = []

    def add_check(name, passed):
        checks.append({"name": name, "passed": passed})

    try:
        # 1. Reset demo
        reset_demo_state(db)

        # 2. Calculate initial route
        res_route = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")
        passed_route = res_route.get("selected_next_hop") == "HUB-B"
        add_check("initial_route_selects_HUB_B", passed_route)

        # 3. Simulate valid scan at HUB-A
        scan_req = ScanRequest(
            parcel_id="MED-104",
            hub_id="HUB-A",
            scanner_id="SCANNER-07",
            gps={"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
            temperature_c=24.3,
            carrier_type="van",
            tamper=False,
        )
        res_scan = await process_and_broadcast_scan(db, scan_req)
        passed_scan = res_scan.get("decision") == "ACCEPTED"
        add_check("valid_scan_accepts", passed_scan)

        # 4. Reset demo again
        reset_demo_state(db)

        # 5. Simulate overload HUB-B
        hub_b = db.get(Hub, "HUB-B")
        if hub_b:
            hub_b.status = "overloaded"
            hub_b.congestion = 0.90
            db.commit()

        res_overload = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")
        passed_overload = res_overload.get("selected_next_hop") == "HUB-D"
        add_check("overload_reroutes_to_HUB_D", passed_overload)

        # 6. Reset demo again
        reset_demo_state(db)

        # 7. Simulate fake scan at HUB-C
        fake_scan_req = ScanRequest(
            parcel_id="MED-104",
            hub_id="HUB-C",
            scanner_id="FAKE-SCANNER",
            rfid_verified=True,
            qr_verified=True,
            gps={"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20},
            temperature_c=24.3,
            carrier_type="van",
            tamper=False,
        )
        res_fake_scan = await process_and_broadcast_scan(db, fake_scan_req)
        passed_fake = res_fake_scan.get("decision") == "BLOCKED"
        add_check("fake_scan_blocks", passed_fake)

        # 8. Verify HUB-C trust drops
        hub_c = db.get(Hub, "HUB-C")
        passed_trust = hub_c is not None and hub_c.trust_score < 0.65
        add_check("trust_score_updates", passed_trust)

    except Exception:
        # If any check fails, fill in blanks to avoid crash
        names = [
            "initial_route_selects_HUB_B",
            "valid_scan_accepts",
            "overload_reroutes_to_HUB_D",
            "fake_scan_blocks",
            "trust_score_updates"
        ]
        existing_names = {c["name"] for c in checks}
        for n in names:
            if n not in existing_names:
                add_check(n, False)
    finally:
        # 9. Reset demo state at the end
        reset_demo_state(db)

    all_passed = all(c["passed"] for c in checks) and len(checks) == 5
    status = "passed" if all_passed else "failed"
    message = "Demo flow validation passed." if all_passed else "Demo flow validation failed."

    return {
        "status": status,
        "checks": checks,
        "message": message,
    }
