# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Verify hardware contracts (BLE tags, ESP-NOW, P2P handshakes) and ledger integration.

from fastapi.testclient import TestClient
from app.main import app


def test_p2p_handshake_ledger():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Call P2P handshake
        res = client.post(
            "/hardware/p2p-handshake",
            json={
                "sender_hub": "HUB-A",
                "receiver_hub": "HUB-B",
                "parcel_id": "MED-104",
                "message_type": "TRUST_SYNC",
                "trust_delta": 0.02,
                "eta_sec": 300
            }
        )
        assert res.status_code == 200
        assert res.json()["status"] == "success"

        # Check ledger
        events = client.get("/ledger/events").json()["events"]
        assert any(e["event_type"] == "p2p_handshake" for e in events)


def test_hardware_scan_contracts():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        # Post scan with BLE fields
        res = client.post(
            "/hardware/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "ESP32-HUB-A",
                "rfid_verified": True,
                "ble_verified": True,
                "ble_parcel_id": "MED-104",
                "ble_rssi_m": -65,
                "ble_temperature_c": 22.4,
                "temperature_c": 23.5,
                "tamper": False,
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 10}
            }
        )
        assert res.status_code == 200
        assert res.json()["status"] == "hardware_scan_completed"

        # Post scan with ESP-NOW prior acceptance
        res2 = client.post(
            "/hardware/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "ESP32-HUB-A",
                "rfid_verified": True,
                "temperature_c": 24.1,
                "tamper": False,
                "esp_now_prior_acceptance": True,
                "esp_now_prior_hub": "HUB-B",
                "esp_now_trust_delta": 0.02,
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 12}
            }
        )
        assert res2.status_code == 200
        assert res2.json()["status"] == "hardware_scan_completed"
