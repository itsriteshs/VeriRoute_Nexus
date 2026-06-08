# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Test Advanced Proofs (TOTP, BLE Mesh, Z-Score Anomaly)

import hmac
import hashlib
import time
import struct
from datetime import datetime, UTC, timedelta

from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal
from app.db.models import Event, Hub, Parcel
from app.engines.immune_engine import check_statistical_anomaly
from app.schemas.scan_schema import ScanRequest


def generate_totp(secret: str, interval: int = 30) -> str:
    t = int(time.time() / interval)
    key = secret.encode("utf-8")
    msg = struct.pack(">Q", t)
    h = hmac.new(key, msg, hashlib.sha256).digest()
    offset = h[-1] & 0x0f
    code = ((h[offset] & 0x7f) << 24 |
            (h[offset + 1] & 0xff) << 16 |
            (h[offset + 2] & 0xff) << 8 |
            (h[offset + 3] & 0xff))
    return f"{code % 1000000:06d}"


def test_zero_trust_totp_handshake():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()
        
        # Valid token
        token = generate_totp("MED-104_packetflow_secret_key")
        response = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "totp_token": token,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "ACCEPTED"
        assert data["immune_checks"]["zero_trust_handshake"] == "PASS"

        # Invalid token
        response_invalid = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "totp_token": "999999",
            },
        )
        assert response_invalid.status_code == 200
        data_invalid = response_invalid.json()
        assert data_invalid["decision"] == "WARNING"
        assert data_invalid["immune_checks"]["zero_trust_handshake"] == "WARN"


def test_mesh_consensus_witnesses():
    with TestClient(app) as client:
        client.post("/demo/seed").raise_for_status()
        
        # Valid active witness
        response = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "witness_node_ids": ["HUB-B"],
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["decision"] == "ACCEPTED"
        assert data["immune_checks"]["mesh_consensus"] == "PASS"

        # Empty/invalid witnesses
        response_invalid = client.post(
            "/scan",
            json={
                "parcel_id": "MED-104",
                "hub_id": "HUB-A",
                "scanner_id": "SCANNER-07",
                "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
                "temperature_c": 24.3,
                "carrier_type": "van",
                "witness_node_ids": [],
            },
        )
        assert response_invalid.status_code == 200
        data_invalid = response_invalid.json()
        assert data_invalid["decision"] == "WARNING"
        assert data_invalid["immune_checks"]["mesh_consensus"] == "WARN"


def test_statistical_anomaly_math():
    db = SessionLocal()
    try:
        # Seed test hub and parcel
        hub = db.get(Hub, "HUB-A")
        parcel = db.get(Parcel, "MED-104")
        
        # Delete old events for HUB-A to start fresh
        db.query(Event).filter(Event.hub_id == "HUB-A").delete()
        db.commit()
        
        # Add 5 events spaced out by 60 seconds (1 minute), with the last one 1 second ago
        base_now = datetime.now(UTC)
        for i in range(5):
            evt_time = base_now - timedelta(seconds=(4 - i) * 60 + 1)
            db.add(Event(
                event_type="scan_received",
                parcel_id="MED-104",
                hub_id="HUB-A",
                timestamp=evt_time.isoformat(),
                decision="ACCEPTED",
            ))
        db.commit()
        
        # Run check_statistical_anomaly immediately (interval ~0, expected interval = 60s)
        # Z-score should be extremely high, triggering statistical anomaly block
        scan_req = ScanRequest(
            parcel_id="MED-104",
            hub_id="HUB-A",
            scanner_id="SCANNER-07",
            gps={"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
            temperature_c=24.3,
        )
        status, reason, trace = check_statistical_anomaly(db, parcel, hub, scan_req)
        assert status == "FAIL"
        assert "Statistical anomaly detected" in reason
        assert trace["z_score"] > 3.0
    finally:
        db.close()
