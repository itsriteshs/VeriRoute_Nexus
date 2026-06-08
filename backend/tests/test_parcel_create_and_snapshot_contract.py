from fastapi.testclient import TestClient

from app.main import app


def test_create_parcel_upserts_and_returns_initial_route():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        res = client.post(
            "/parcels",
            json={
                "id": "MED-104",
                "parcel_type": "medicine",
                "source_hub": "HUB-A",
                "destination_hub": "CUSTOMER-ZONE",
                "priority": "high",
                "sla_minutes": 45,
                "temperature_limit": 25.0,
                "carrier_type": "van",
            },
        )

        assert res.status_code == 200
        data = res.json()
        assert data["parcel"]["id"] == "MED-104"
        assert data["parcel"]["current_hub"] == "HUB-A"
        assert data["initial_route"]["selected_next_hop"] == "HUB-B"
        assert data["initial_route"]["full_route"] == ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]
        assert data["initial_route"]["candidate_scores"]

        events = client.get("/ledger/events").json()["events"]
        assert any(event["event_type"] == "parcel_created" and event["action"] == "CREATE_OR_UPSERT_PARCEL" for event in events)


def test_demo_snapshot_matches_frontend_live_contract():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()
        client.post(
            "/route/next-hop",
            json={
                "parcel_id": "MED-104",
                "current_hub": "HUB-A",
                "destination_hub": "CUSTOMER-ZONE",
            },
        ).raise_for_status()

        res = client.get("/demo/snapshot")

        assert res.status_code == 200
        data = res.json()
        assert len(data["hubs"]) == 7
        assert len(data["edges"]) == 8
        assert data["parcels"][0]["id"] == "MED-104"
        assert data["latest_route"]["full_route"] == ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]
        assert data["latest_route"]["candidate_scores"]
        assert data["latest_route"]["reason"]
        assert "created_at" in data["latest_route"]
        assert "latest_events" in data
        assert "active_disruptions" in data
