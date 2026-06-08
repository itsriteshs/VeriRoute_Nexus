# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Verify routing behavior under fail, overload, traffic, weather, and temperature scenarios.

from fastapi.testclient import TestClient
from app.main import app


def test_fail_hub_avoids_it():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Fail HUB-B
        fail_res = client.post(
            "/scenario/fail-hub",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-B"
            }
        )
        assert fail_res.status_code == 200
        assert fail_res.json()["disruption"]["type"] == "hub_failed"

        # Hub B should be avoided
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


def test_overload_hub_avoids_where_possible():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Overload HUB-B
        overload_res = client.post(
            "/scenario/overload-hub",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-B",
                "congestion": 0.95
            }
        )
        assert overload_res.status_code == 200

        # Hub B should be avoided in favor of D
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


def test_traffic_jam_and_weather_risk():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Apply traffic jam on A->B
        traffic_res = client.post(
            "/scenario/traffic-jam",
            json={
                "parcel_id": "MED-104",
                "from_hub": "HUB-A",
                "to_hub": "HUB-B",
                "traffic_risk": 0.85
            }
        )
        assert traffic_res.status_code == 200

        # Apply weather risk on A->B
        weather_res = client.post(
            "/scenario/weather-risk",
            json={
                "parcel_id": "MED-104",
                "from_hub": "HUB-A",
                "to_hub": "HUB-B",
                "weather_risk": 0.90
            }
        )
        assert weather_res.status_code == 200

        # Events ledger should contain traffic_jam and weather_risk
        events = client.get("/ledger/events").json()["events"]
        assert any(e["event_type"] == "traffic_jam" for e in events)
        assert any(e["event_type"] == "weather_risk" for e in events)


def test_temp_breach():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Apply temp breach
        breach_res = client.post(
            "/scenario/temp-breach",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "temperature_c": 29.5
            }
        )
        assert breach_res.status_code == 200
        assert breach_res.json()["cold_chain_status"] == "BREACH"

        # Events ledger should contain temperature_breach
        events = client.get("/ledger/events").json()["events"]
        assert any(e["event_type"] == "temperature_breach" for e in events)
