# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Phase 7/8 hardware scan and dual-node handshakes regression tests.

from fastapi.testclient import TestClient
from app.main import app


def test_hardware_scan_requires_gps():
    with TestClient(app) as client:
        # Seed DB
        client.post("/demo/seed").raise_for_status()

        # Connect to websocket
        with client.websocket_connect("/ws") as websocket:
            # Post hardware scan without GPS
            response = client.post(
                "/hardware/scan",
                json={
                    "parcel_id": "MED-104",
                    "hub_id": "HUB-A",
                    "scanner_id": "ESP32-HUB-A",
                    "rfid_verified": True,
                    "temperature_c": 24.3,
                    "tamper": False,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "hardware_scan_received"
            assert data["requires_gps"] is True
            assert data["gps_scan_url"] == "/scan/HUB-A?parcel_id=MED-104"
            assert data["hardware_context"]["rfid_verified"] is True
            assert data["hardware_context"]["ble_verified"] is False

            # Assert ws message received
            msg = websocket.receive_json()
            assert msg["type"] == "hardware_scan_received"
            assert msg["payload"]["parcel_id"] == "MED-104"
            assert msg["payload"]["hub_id"] == "HUB-A"


def test_hardware_scan_with_gps_runs_immunenet():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            # Post hardware scan with GPS
            response = client.post(
                "/hardware/scan",
                json={
                    "parcel_id": "MED-104",
                    "hub_id": "HUB-A",
                    "scanner_id": "ESP32-HUB-A",
                    "rfid_verified": True,
                    "temperature_c": 24.3,
                    "tamper": False,
                    "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "hardware_scan_completed"
            assert data["requires_gps"] is False
            assert data["decision"] == "ACCEPTED"
            assert data["led"] == "GREEN"
            assert data["immune_checks"]["geofence"] == "PASS"

            # Assert ws events: scan_received, movement_accepted, metrics_updated, hardware_scan_completed
            events = []
            for _ in range(7):
                msg = websocket.receive_json()
                events.append(msg)

            types = [e["type"] for e in events]
            assert "scan_received" in types
            assert "movement_accepted" in types
            assert "hardware_scan_completed" in types


def test_ble_tag_identity_mismatch():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        response = client.post(
            "/hardware/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "ESP32-HUB-A",
                "rfid_verified": True,
                "ble_verified": True,
                "ble_parcel_id": "WRONG-TAG-104",
                "temperature_c": 24.3,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["hardware_context"]["ble_identity_mismatch"] is True


def test_p2p_handshake_updates_trust_score():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()

        with client.websocket_connect("/ws") as websocket:
            # Verify initial trust of HUB-B is 0.92
            hubs_res = client.get("/hubs").json()["hubs"]
            hub_b = next(h for h in hubs_res if h["id"] == "HUB-B")
            assert hub_b["trust_score"] == 0.92

            # Post P2P handshake from HUB-A to HUB-B with trust_delta
            response = client.post(
                "/hardware/p2p-handshake",
                json={
                    "sender_hub": "HUB-A",
                    "receiver_hub": "HUB-B",
                    "parcel_id": "MED-104",
                    "message_type": "TRUST_SYNC",
                    "trust_delta": 0.02,
                    "eta_sec": 300,
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"

            # Check new trust score (0.92 updated with Bayesian alpha increment)
            hubs_res_after = client.get("/hubs").json()["hubs"]
            hub_b_after = next(h for h in hubs_res_after if h["id"] == "HUB-B")
            assert hub_b_after["trust_score"] == 0.92

            # Assert ws events: p2p_handshake, trust_updated, metrics_updated
            events = []
            for _ in range(3):
                msg = websocket.receive_json()
                events.append(msg)

            types = [e["type"] for e in events]
            assert "p2p_handshake" in types
            assert "trust_updated" in types
            assert "metrics_updated" in types
