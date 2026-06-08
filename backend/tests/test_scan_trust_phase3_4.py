# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Phase 3/4 ImmuneNet and trust scoring smoke tests.

from fastapi.testclient import TestClient

from app.main import app


def test_valid_scan_accepts_and_updates_trust_route_and_ledger():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        response = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "tamper": False,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "ACCEPTED"
        assert data["led"] == "GREEN"
        assert data["immune_checks"]["geofence"] == "PASS"
        assert data["trust_update"]["new_score"] == 0.99
        assert data["route_decision"]["selected_next_hop"] == "HUB-B"
        events = client.get("/ledger/events").json()["events"]
        assert any(event["event_type"] == "movement_accepted" for event in events)


def test_fake_scan_blocks_geofence_and_drops_hub_trust():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        response = client.post(
            "/scan/fake",
            json={
                "parcel_id": "MED-104",
                "claimed_hub": "HUB-C",
                "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20},
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "BLOCKED"
        assert data["led"] == "RED"
        assert data["failed_checks"] == ["geofence"]
        assert data["trust_update"]["hub_id"] == "HUB-C"
        assert data["trust_update"]["new_score"] == 0.5
        events = client.get("/ledger/events").json()["events"]
        assert any(event["event_type"] == "fake_scan_blocked" for event in events)
        parcel = client.get("/parcels/MED-104").json()["parcel"]
        assert parcel["current_hub"] == "HUB-A"


def test_clone_tamper_and_cold_chain_decisions():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()
        clone = client.post("/scan/clone", json={"parcel_id": "MED-104", "first_hub": "HUB-B", "second_hub": "HUB-D"})
        assert clone.status_code == 200
        assert clone.json()["decision"] == "BLOCKED"
        assert clone.json()["failed_checks"] == ["clone_scan"]

        client.post("/demo/seed").raise_for_status()
        tamper = client.post("/scan/tamper", json={"parcel_id": "MED-104", "hub_id": "HUB-C", "tamper": True})
        assert tamper.status_code == 200
        assert tamper.json()["decision"] == "HOLD"
        assert tamper.json()["action"] == "ALERT_AND_HOLD"

        client.post("/demo/seed").raise_for_status()
        cold = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 29.2,
                "carrier_type": "van",
            },
        )
        assert cold.status_code == 200
        assert cold.json()["decision"] == "REROUTED"
        assert cold.json()["led"] == "AMBER"
        assert cold.json()["failed_checks"] == ["cold_chain"]
