# VeriRoute Nexus

**Team:** Aristotle
**Tagline:** Proof-powered routing for trusted logistics.

VeriRoute Nexus verifies every parcel handoff before routing continues. It combines PacketFlow routing, Proof-of-Movement verification, ImmuneNet anomaly detection, AgentOps disruption response, SwarmFlow Smart Relay Hub hardware, and a Digital Twin command center.

## System Layers

| Layer | Purpose | Owner |
| --- | --- | --- |
| PacketFlow | Dynamic next-hop routing for parcels | Person 1 |
| Proof-of-Movement | GPS/geofence + identity + sensor verification for handoffs | Person 1 + Person 3 |
| ImmuneNet | Fake scan, clone scan, impossible movement, cold-chain, and tamper detection | Person 1 |
| AgentOps | Autonomous disruption response and rerouting | Person 1 + Person 2 |
| SwarmFlow | ESP32/RFID/QR/GPS/temperature/LED proof layer | Person 3 |
| Digital Twin | Hubs, parcels, trust, reroutes, alerts, and metrics UI | Person 2 |

## Ownership

| Person | Role | Folders | Progress File |
| --- | --- | --- | --- |
| Person 1 | Backend + Algorithms Lead | `backend/`, API contracts, demo data | `what_is_done_person_1.md` |
| Person 2 | Frontend + Digital Twin + UX Lead | `frontend/` | `what_is_done_person_2.md` |
| Person 3 | Hardware + Demo + Presentation Lead | `hardware/`, `presentation/` | `what_is_done_person_3.md` |

## Quick Start

Backend start command:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

Frontend start command:

```bash
cd frontend
npm install
npm run dev
```

The `hardware/` folder contains ESP32 firmware placeholders, bridge scripts, pin maps, QR payloads, CAD placeholders, and PCB/story notes.

## Demo Flow

Reset demo, create `MED-104`, scan at `HUB-A`, show PacketFlow route and score breakdown, fail or overload `HUB-B`, show AgentOps reroute, inject fake scan, show ImmuneNet block and trust decay, trigger temperature breach, show cold-chain reroute, then show impact metrics.

Final line: **We are not tracking parcels. We are proving movement.**

## Repository Structure

- `backend/`: FastAPI starter, schemas, engines, routes, tests.
- `frontend/`: React/Vite starter Digital Twin.
- `hardware/`: Smart Relay Hub firmware and bridge placeholders.
- `data/`: Demo hubs, edges, parcels, and scenarios.
- `docs/`: Architecture, contracts, planning, research, and assets.
- `presentation/`: Slides, scripts, judge Q&A, screenshots, and fallback plan.
- `.github/`: Pull request and issue templates.

## Integration Rule

All API contracts must be updated in `API_CONTRACT.md` before implementation changes. Any PR changing request payloads, response payloads, WebSocket events, or demo data shape must mention the contract update.

## Future Phase: Hardware Integration

Person 3's upgraded hardware plan is a Dual-Node SwarmFlow Relay Network with physical `HUB-A` and `HUB-B` SmartHub nodes, an ESP-NOW peer-to-peer handshake path, and an ESP32-C3 BLE Smart Parcel Tag. The backend now exposes direct hardware scan and peer-to-peer handshake endpoints for rehearsal.

- `POST /hardware/scan` accepts device-native fields from `hardware_submission`: `device_id`, `button_pressed`, flat `lat`/`lng`, optional BLE fields, and optional ESP-NOW cache fields.
- If GPS is missing, `POST /hardware/scan` returns `requires_gps: true` plus `/scan/{hub_id}?parcel_id=...` for the phone GPS handoff.
- `POST /hardware/p2p-handshake` logs `p2p_handshake` events between `HUB-A` and `HUB-B`.

The event ledger stores `event_type` as text and `raw_payload` as JSON text so ESP-NOW/BLE metadata can be recorded without changing `GET /ledger/events`.

## Phase 2: PacketFlow Routing

PacketFlow routing is implemented as a deterministic next-hop decision layer. It scores active candidate routes using SLA risk, candidate congestion, hub trust risk, condition/cold-chain risk, and cost/emission score:

```text
0.30 * sla_risk + 0.25 * congestion_risk + 0.20 * trust_risk + 0.15 * condition_risk + 0.10 * cost_emission_score
```

For the seeded `MED-104` parcel at `HUB-A`, `POST /route/next-hop` selects `HUB-B` and returns the route `HUB-A -> HUB-B -> HUB-E -> CUSTOMER-ZONE`. Phase 2 does not implement scan validation, trust decay, AgentOps, WebSockets, hardware scan, ESP-NOW endpoints, BLE parsing, fake scan, clone scan, or temperature breach flows.

## Phase 3 + 4: ImmuneNet Scan Validation And Trust

ImmuneNet validates every scan as a movement claim using geofence, speed plausibility, route graph, clone scan, cold-chain, and tamper checks. The trust engine updates hub trust after each scan and records trust history. Accepted and rerouted scans recalculate PacketFlow routes.

Demo commands:

```bash
curl -X POST http://localhost:8000/demo/seed

curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":24.3,"carrier_type":"van","tamper":false}'

curl -X POST http://localhost:8000/scan/fake \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","claimed_hub":"HUB-C","fake_gps":{"lat":11.1000,"lng":77.1000,"accuracy_m":20}}'

curl -X POST http://localhost:8000/scan/clone \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","first_hub":"HUB-B","second_hub":"HUB-D"}'

curl -X POST http://localhost:8000/scan/tamper \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-C","tamper":true}'

curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":29.2,"carrier_type":"van","tamper":false}'

curl http://localhost:8000/trust/hubs
curl http://localhost:8000/trust/history/HUB-C
curl http://localhost:8000/ledger/events
curl http://localhost:8000/metrics
```

Expected demo behavior: valid scan returns `ACCEPTED` and `GREEN`; fake scan returns `BLOCKED` and `RED`; clone scan returns `BLOCKED` with `clone_scan`; tamper scan returns `HOLD`; hot cold-chain scan returns `REROUTED` and `AMBER`.

## Phase 5 + 6: WebSocket Live Broadcasting & AgentOps Scenario Engine

FastAPI WebSocket connection manages live real-time events on `ws://localhost:8000/ws`.

### WebSocket Message Envelope Format
```json
{
  "type": "event_type_here",
  "timestamp": "2026-06-08T10:42:00Z",
  "payload": {}
}
```

### Scenario APIs
AgentOps handles autonomous routing replans and logs disruptions under five simulated disaster scenarios:

* **Fail Hub** (`POST /scenario/fail-hub`): Avoids the failed hub.
* **Overload Hub** (`POST /scenario/overload-hub`): Shifts candidate routing risk away from the overloaded hub.
* **Traffic Jam** (`POST /scenario/traffic-jam`): Increases routing ETA for affected edges.
* **Weather Risk** (`POST /scenario/weather-risk`): Increases edge weather risk and condition risk for sensitive parcels.
* **Temperature Breach** (`POST /scenario/temp-breach`): Triggers temperature breach alerts and reroutes parcels to cold-chain hubs.

### Curl Commands
```bash
# Overload HUB-B
curl -X POST http://localhost:8000/scenario/overload-hub \
  -H "Content-Type: application/json" \
  -d '{"hub_id":"HUB-B","parcel_id":"MED-104","congestion":0.95}'

# Fail HUB-B
curl -X POST http://localhost:8000/scenario/fail-hub \
  -H "Content-Type: application/json" \
  -d '{"hub_id":"HUB-B","parcel_id":"MED-104"}'

# Traffic jam HUB-B -> HUB-E
curl -X POST http://localhost:8000/scenario/traffic-jam \
  -H "Content-Type: application/json" \
  -d '{"from_hub":"HUB-B","to_hub":"HUB-E","parcel_id":"MED-104","traffic_risk":0.95}'

# Weather risk HUB-B -> HUB-E
curl -X POST http://localhost:8000/scenario/weather-risk \
  -H "Content-Type: application/json" \
  -d '{"from_hub":"HUB-B","to_hub":"HUB-E","parcel_id":"MED-104","weather_risk":0.90}'

# Temperature breach MED-104
curl -X POST http://localhost:8000/scenario/temp-breach \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-A","temperature_c":29.2}'
```

### Python WebSocket Tester
Use the following snippet to subscribe to the live stream:
```python
import asyncio, websockets, json
async def main():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        print("Connected to VeriRoute WS")
        while True:
            print(json.dumps(json.loads(await ws.recv()), indent=2))
asyncio.run(main())
```

Phase 7 will implement hardware scan integration next.
