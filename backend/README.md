# Backend

Owner: Person 1 — Backend + Algorithms Lead

FastAPI Phase 1 and Phase 2 backend foundation. Keep API changes synced with root `API_CONTRACT.md`.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Or use:

```bash
./run.sh
```

## Seed Demo Data

```bash
curl -X POST http://localhost:8000/demo/seed
```

This clears and recreates the Phase 1 demo graph, `MED-104`, the initial `parcel_created` event, and a `system_ready` event whose `raw_payload` marks `HUB-A` and `HUB-B` as future physical dual-node SwarmFlow hardware nodes.

## Test Endpoints

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/demo/seed
curl http://localhost:8000/hubs
curl http://localhost:8000/edges
curl http://localhost:8000/parcels
curl -X POST http://localhost:8000/route/next-hop \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","current_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE"}'
curl http://localhost:8000/route/MED-104
curl http://localhost:8000/route/decisions
curl http://localhost:8000/ledger/events
curl http://localhost:8000/metrics
```

## Phase 3 + 4 ImmuneNet And Trust

```bash
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

curl http://localhost:8000/trust/hubs
curl http://localhost:8000/trust/history/HUB-C
```

Valid scans return `GREEN`, fake and clone scans return `RED`, tamper returns `HOLD`, and hot cold-chain scans return `AMBER`. Trust changes are visible through `/trust/hubs` and `/trust/history/{hub_id}`.

## Phase 2 PacketFlow Routing

Phase 2 adds route calculation and route decision persistence only. PacketFlow evaluates active neighbor hubs and persists every `POST /route/next-hop` call to `route_decisions`.

Score formula:

```text
0.30 * sla_risk + 0.25 * congestion_risk + 0.20 * trust_risk + 0.15 * condition_risk + 0.10 * cost_emission_score
```

Expected seeded demo result:

```json
{"parcel_id":"MED-104","selected_next_hop":"HUB-B","full_route":["HUB-A","HUB-B","HUB-E","CUSTOMER-ZONE"]}
```

This keeps `HUB-B` as the initial route target so later demo phases can overload or fail it and reroute through alternatives.

## Phase 1 Boundary

Do not implement WebSocket broadcasting, hardware scan, AgentOps scenario routes, AI API calls, ESP-NOW, or BLE parsing in this phase. The event ledger is prepared for future `p2p_handshake` rows and JSON `raw_payload` metadata, but `/hardware/scan` and `/hardware/p2p-handshake` remain future endpoints.
