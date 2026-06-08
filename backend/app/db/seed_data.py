# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: deterministic Phase 1 demo seed data.

import json

from sqlalchemy.orm import Session

from app.core import constants
from app.db.models import (
    Disruption,
    Edge,
    Event,
    Hub,
    ImmuneCheck,
    Parcel,
    RouteDecision,
    TrustHistory,
)
from app.utils.time_utils import utc_now_iso

HUBS = [
    {"id": "HUB-A", "name": "Central Smart Hub A", "lat": 11.0168, "lng": 76.9558, "trust_score": 0.98, "status": "active", "congestion": 0.20, "cold_chain": False, "alpha": 98, "beta": 2},
    {"id": "HUB-B", "name": "Relay Hub B", "lat": 11.0250, "lng": 76.9650, "trust_score": 0.92, "status": "active", "congestion": 0.50, "cold_chain": False, "alpha": 92, "beta": 8},
    {"id": "HUB-C", "name": "Relay Hub C", "lat": 11.0350, "lng": 76.9750, "trust_score": 0.65, "status": "active", "congestion": 0.25, "cold_chain": False, "alpha": 65, "beta": 35},
    {"id": "COLD-HUB-C", "name": "Cold Chain Hub C", "lat": 11.0400, "lng": 76.9800, "trust_score": 0.95, "status": "active", "congestion": 0.30, "cold_chain": True, "alpha": 95, "beta": 5},
    {"id": "HUB-D", "name": "South Relay Hub D", "lat": 11.0050, "lng": 76.9700, "trust_score": 0.90, "status": "active", "congestion": 0.20, "cold_chain": False, "alpha": 90, "beta": 10},
    {"id": "HUB-E", "name": "Final Relay Hub E", "lat": 11.0450, "lng": 76.9900, "trust_score": 0.88, "status": "active", "congestion": 0.35, "cold_chain": True, "alpha": 88, "beta": 12},
    {"id": "CUSTOMER-ZONE", "name": "Customer Delivery Zone", "lat": 11.0550, "lng": 77.0000, "trust_score": 1.0, "status": "active", "congestion": 0.10, "cold_chain": False, "alpha": 100, "beta": 0},
]

EDGES = [
    {"from_hub": "HUB-A", "to_hub": "HUB-B", "distance_km": 4.5, "eta_min": 12, "traffic_risk": 0.2, "cost_score": 0.3},
    {"from_hub": "HUB-A", "to_hub": "HUB-D", "distance_km": 5.2, "eta_min": 15, "traffic_risk": 0.25, "cost_score": 0.35},
    {"from_hub": "HUB-B", "to_hub": "HUB-E", "distance_km": 6.0, "eta_min": 14, "traffic_risk": 0.25, "cost_score": 0.4},
    {"from_hub": "HUB-D", "to_hub": "HUB-E", "distance_km": 7.0, "eta_min": 18, "traffic_risk": 0.20, "cost_score": 0.45},
    {"from_hub": "HUB-A", "to_hub": "HUB-C", "distance_km": 5.8, "eta_min": 13, "traffic_risk": 0.15, "cost_score": 0.32},
    {"from_hub": "HUB-C", "to_hub": "COLD-HUB-C", "distance_km": 1.5, "eta_min": 5, "traffic_risk": 0.1, "cost_score": 0.2},
    {"from_hub": "COLD-HUB-C", "to_hub": "HUB-E", "distance_km": 4.0, "eta_min": 11, "traffic_risk": 0.2, "cost_score": 0.3},
    {"from_hub": "HUB-E", "to_hub": "CUSTOMER-ZONE", "distance_km": 3.5, "eta_min": 9, "traffic_risk": 0.1, "cost_score": 0.2},
]


def seed_demo_data(db: Session) -> dict[str, object]:
    for model in (TrustHistory, RouteDecision, ImmuneCheck, Disruption, Event, Parcel, Edge, Hub):
        db.query(model).delete()

    now = utc_now_iso()
    db.add_all(Hub(created_at=now, updated_at=now, **hub) for hub in HUBS)
    db.add_all(Edge(**edge) for edge in EDGES)
    db.add(
        Parcel(
            id="MED-104",
            parcel_type="medicine",
            source_hub="HUB-A",
            destination_hub="CUSTOMER-ZONE",
            current_hub="HUB-A",
            previous_hub=None,
            priority="high",
            sla_minutes=45,
            temperature_limit=25.0,
            current_temperature=24.3,
            carrier_type="van",
            status="created",
            trust_state="unverified",
            created_at=now,
            updated_at=now,
        )
    )
    db.add(
        Event(
            event_type=constants.PARCEL_CREATED,
            parcel_id="MED-104",
            hub_id="HUB-A",
            timestamp=now,
            decision="CREATED",
            action="SEED_DEMO_PARCEL",
            severity="info",
            reason="Demo medicine parcel MED-104 created at HUB-A.",
        )
    )
    db.add(
        Event(
            event_type=constants.SYSTEM_READY,
            parcel_id=None,
            hub_id=None,
            timestamp=now,
            decision="READY",
            action="DUAL_NODE_HARDWARE_READY",
            severity="info",
            reason="Demo seeded with HUB-A and HUB-B prepared for upgraded dual-node SwarmFlow relay integration.",
            raw_payload=json.dumps(
                {
                    "hardware_mode": "dual_node_swarmflow",
                    "physical_nodes": ["HUB-A", "HUB-B"],
                    "future_protocols": ["BLE parcel tag", "ESP-NOW p2p_handshake"],
                }
            ),
        )
    )
    db.commit()
    return {"status": "seeded", "hubs": len(HUBS), "edges": len(EDGES), "demo_parcel": "MED-104"}
