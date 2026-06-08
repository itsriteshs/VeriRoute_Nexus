# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Phase 2 PacketFlow routing smoke tests.

from fastapi.testclient import TestClient

from app.main import app


def test_seeded_med_104_selects_hub_b_route():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        response = client.post(
            "/route/next-hop",
            json={
                "parcel_id": "MED-104",
                "current_hub": "HUB-A",
                "destination_hub": "CUSTOMER-ZONE",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["selected_next_hop"] == "HUB-B"
        assert data["full_route"] == ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]
        assert any(candidate["hub_id"] == "HUB-B" and candidate["selected"] for candidate in data["candidate_scores"])


def test_route_decision_history_returns_parsed_json_arrays():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()
        client.post("/route/next-hop", json={"parcel_id": "MED-104"}).raise_for_status()

        response = client.get("/route/decisions")

        assert response.status_code == 200
        data = response.json()
        assert data[0]["parcel_id"] == "MED-104"
        assert data[0]["full_route"] == ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]
        assert isinstance(data[0]["candidate_scores"], list)
