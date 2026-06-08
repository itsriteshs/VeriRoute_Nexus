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


def test_hardware_submission_native_payload_contract():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        res = client.post(
            "/hardware/scan",
            json={
                "device_id": "ESP32-HUB-A-01",
                "hub_id": "HUB-A",
                "parcel_id": "MED-104",
                "rfid_uid": "RFID4A8B9C104",
                "qr_payload": "http://localhost:5173/scan/HUB-A?parcel_id=MED-104",
                "temperature_c": 24.3,
                "button_pressed": False,
                "lat": 11.0168,
                "lng": 76.9558,
                "timestamp": "2026-06-08T15:00:00Z",
                "ble_verified": True,
                "ble_rssi_m": 1.2,
                "esp_now_prior_acceptance": False,
                "esp_now_prior_hub": "",
                "esp_now_trust_delta": 0.0,
            },
        )

        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "hardware_scan_completed"
        assert data["accepted"] is True
        assert data["decision"] == "ACCEPTED"
        assert data["led"] == "GREEN"
        assert data["message"]
        assert data["hardware_context"]["scanner_id"] == "ESP32-HUB-A-01"


def test_hardware_submission_without_gps_returns_phone_scan_url():
    with TestClient(app) as client:
        client.post("/demo/reset").raise_for_status()

        res = client.post(
            "/hardware/scan",
            json={
                "device_id": "ESP32-HUB-A-01",
                "hub_id": "HUB-A",
                "parcel_id": "MED-104",
                "rfid_uid": "RFID4A8B9C104",
                "qr_payload": "http://localhost:5173/scan/HUB-A?parcel_id=MED-104",
                "temperature_c": 24.3,
                "button_pressed": False,
            },
        )

        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "hardware_scan_received"
        assert data["accepted"] is False
        assert data["requires_gps"] is True
        assert data["gps_scan_url"] == "/scan/HUB-A?parcel_id=MED-104"
        assert data["message"] == "RFID and temperature captured. Awaiting phone GPS proof."
        assert data["hardware_context"]["scanner_id"] == "ESP32-HUB-A-01"
