# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Phase 9 demo flow and diagnostic endpoint verification.

from fastapi.testclient import TestClient
from app.main import app


def test_demo_reset_and_ready():
    with TestClient(app) as client:
        # Reset demo
        res = client.post("/demo/reset")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "reset_complete"
        assert data["demo_parcel"] == "MED-104"

        # Ready check
        ready_res = client.get("/ready")
        assert ready_res.status_code == 200
        ready_data = ready_res.json()
        assert ready_data["ready"] is True
        assert ready_data["checks"]["database"] is True


def test_initial_routing_and_scan_flow():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Route next hop for MED-104 at HUB-A should be HUB-B
        route_res = client.post(
            "/route/next-hop",
            json={
                "parcel_id": "MED-104",
                "current_hub": "HUB-A",
                "destination_hub": "CUSTOMER-ZONE"
            }
        )
        assert route_res.status_code == 200
        assert route_res.json()["selected_next_hop"] == "HUB-B"

        # Valid scan at HUB-A
        scan_res = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "tamper": False
            }
        )
        assert scan_res.status_code == 200
        assert scan_res.json()["decision"] == "ACCEPTED"


def test_fake_scan_and_trust_decay():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Fake scan at HUB-C
        fake_res = client.post(
            "/scan/fake",
            json={
                "parcel_id": "MED-104",
                "claimed_hub": "HUB-C",
                "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20}
            }
        )
        assert fake_res.status_code == 200
        assert fake_res.json()["decision"] == "BLOCKED"

        # Check trust score of HUB-C has dropped (original 0.65)
        hubs_res = client.get("/hubs").json()["hubs"]
        hub_c = next(h for h in hubs_res if h["id"] == "HUB-C")
        assert hub_c["trust_score"] < 0.65


def test_overload_hub_reroutes():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Overload HUB-B
        overload_res = client.post(
            "/scenario/overload-hub",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-B",
                "congestion": 0.90
            }
        )
        assert overload_res.status_code == 200

        # Rerouted next-hop should avoid B and select HUB-D
        route_res = client.post(
            "/route/next-hop",
            json={
                "parcel_id": "MED-104",
                "current_hub": "HUB-A",
                "destination_hub": "CUSTOMER-ZONE"
            }
        )
        assert route_res.status_code == 200
        assert route_res.json()["selected_next_hop"] == "HUB-D"


def test_metrics_updating():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Run multiple checks
        client.post(
            "/scan/fake",
            json={
                "parcel_id": "MED-104",
                "claimed_hub": "HUB-C",
                "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20}
            }
        ).raise_for_status()

        # Get metrics
        metrics_res = client.get("/metrics")
        assert metrics_res.status_code == 200
        m = metrics_res.json()
        assert m["anomalies_blocked"] >= 1
        assert m["fake_scans_blocked"] >= 1
        assert m["ledger_events"] > 2
