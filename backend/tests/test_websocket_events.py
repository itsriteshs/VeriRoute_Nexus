# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Verify WebSocket broadcast envelope consistency (type, timestamp, payload).

from fastapi.testclient import TestClient
from app.main import app


def test_websocket_envelope_format():
    with TestClient(app) as client:
        # Reset demo to ensure DB is in seeded state
        client.post("/demo/reset").raise_for_status()

        # Connect to WS and trigger seed to get events
        with client.websocket_connect("/ws") as ws:
            client.post("/demo/reset").raise_for_status()

            # Read broadcast messages
            msg1 = ws.receive_json()
            assert "type" in msg1
            assert "timestamp" in msg1
            assert "payload" in msg1
            assert msg1["type"] == "demo_reset"
            assert msg1["payload"]["status"] == "reset_complete"

            msg2 = ws.receive_json()
            assert "type" in msg2
            assert "timestamp" in msg2
            assert "payload" in msg2
            assert msg2["type"] == "metrics_updated"
            assert msg2["payload"]["fallback_reliability"] is True
