# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Phase 5/6 scenarios and WebSocket live broadcasting regression tests.

from fastapi.testclient import TestClient
from app.main import app


def test_websocket_connection_and_scenario_broadcasts():
    with TestClient(app) as client:
        # ----------------------------------------------------
        # 1. Test Overload Hub Scenario
        # ----------------------------------------------------
        client.post("/demo/seed").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            status_res = client.get("/ws/status")
            assert status_res.status_code == 200
            assert status_res.json()["active_connections"] == 1

            overload_res = client.post(
                "/scenario/overload-hub",
                json={"hub_id": "HUB-B", "parcel_id": "MED-104", "congestion": 0.95},
            )
            assert overload_res.status_code == 200
            data = overload_res.json()
            assert data["disruption"]["type"] == "hub_overloaded"
            assert data["disruption"]["target"] == "HUB-B"
            assert data["old_route"] == ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]
            assert data["new_route"] == ["HUB-A", "HUB-D", "HUB-E", "CUSTOMER-ZONE"]

            events = []
            for _ in range(4):
                msg = websocket.receive_json()
                events.append(msg)

            event_types = [e["type"] for e in events]
            assert "hub_overloaded" in event_types
            assert "reroute_triggered" in event_types
            assert "route_decision" in event_types
            assert "metrics_updated" in event_types

        # ----------------------------------------------------
        # 2. Test Fail Hub Scenario (using fresh reset)
        # ----------------------------------------------------
        client.post("/demo/reset").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            fail_res = client.post(
                "/scenario/fail-hub", json={"hub_id": "HUB-B", "parcel_id": "MED-104"}
            )
            assert fail_res.status_code == 200
            data = fail_res.json()
            assert data["disruption"]["type"] == "hub_failed"
            assert data["disruption"]["target"] == "HUB-B"
            assert data["new_route"] == ["HUB-A", "HUB-D", "HUB-E", "CUSTOMER-ZONE"]

            events = []
            for _ in range(4):
                msg = websocket.receive_json()
                events.append(msg)
            event_types = [e["type"] for e in events]
            assert "hub_failed" in event_types
            assert "reroute_triggered" in event_types
            assert "route_decision" in event_types
            assert "metrics_updated" in event_types

        # ----------------------------------------------------
        # 3. Test Traffic Jam Scenario (fresh reset)
        # ----------------------------------------------------
        client.post("/demo/reset").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            traffic_res = client.post(
                "/scenario/traffic-jam",
                json={
                    "from_hub": "HUB-B",
                    "to_hub": "HUB-E",
                    "parcel_id": "MED-104",
                    "traffic_risk": 0.95,
                },
            )
            assert traffic_res.status_code == 200
            data = traffic_res.json()
            assert data["disruption"]["type"] == "traffic_jam"

            events = []
            for _ in range(4):
                msg = websocket.receive_json()
                events.append(msg)
            event_types = [e["type"] for e in events]
            assert "traffic_jam" in event_types
            assert "reroute_triggered" in event_types
            assert "route_decision" in event_types
            assert "metrics_updated" in event_types

        # ----------------------------------------------------
        # 4. Test Weather Risk Scenario (fresh reset)
        # ----------------------------------------------------
        client.post("/demo/reset").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            weather_res = client.post(
                "/scenario/weather-risk",
                json={
                    "from_hub": "HUB-B",
                    "to_hub": "HUB-E",
                    "parcel_id": "MED-104",
                    "weather_risk": 0.90,
                },
            )
            assert weather_res.status_code == 200
            data = weather_res.json()
            assert data["disruption"]["type"] == "weather_risk"

            events = []
            for _ in range(4):
                msg = websocket.receive_json()
                events.append(msg)
            event_types = [e["type"] for e in events]
            assert "weather_risk" in event_types
            assert "reroute_triggered" in event_types
            assert "route_decision" in event_types
            assert "metrics_updated" in event_types

        # ----------------------------------------------------
        # 5. Test Temp Breach Scenario (fresh reset)
        # ----------------------------------------------------
        client.post("/demo/reset").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            temp_res = client.post(
                "/scenario/temp-breach",
                json={"parcel_id": "MED-104", "hub_id": "HUB-A", "temperature_c": 29.2},
            )
            assert temp_res.status_code == 200
            data = temp_res.json()
            assert data["decision"] == "REROUTED"
            assert data["action"] == "REROUTE_TO_COLD_HUB"
            assert "COLD-HUB-C" in data["new_route"]

            events = []
            for _ in range(4):
                msg = websocket.receive_json()
                events.append(msg)
            event_types = [e["type"] for e in events]
            assert "temperature_breach" in event_types
            assert "reroute_triggered" in event_types
            assert "route_decision" in event_types
            assert "metrics_updated" in event_types
