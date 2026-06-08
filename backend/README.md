# PacketFlow ImmuneNet Backend

Owner: Person 1 — Backend + Algorithms Lead

FastAPI backend application implementing trust-powered logisitics routing, real-time threat validation (ImmuneNet), simulated network disruptions, and hardware ingest endpoints.

---

## Setup & Running

### Requirements
Ensure you have Python 3.10+ installed.

### Start the Backend Server
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Or use the shortcut script:
```bash
./run.sh
```

---

## API Endpoints List

### Diagnostics & Health
* `GET /health`: Diagnostic details of status, database, and seed state.
* `GET /ready`: Verification checklist for database, hubs, edges, parcel seeding, routing availability, and WebSocket server.

### Demo Seeding & Simulation Control
* `POST /demo/seed`: Clears database tables and seeds initial hubs, edges, parcel `MED-104`, and starter events.
* `POST /demo/reset`: Resets demo state to seeded defaults, broadcasting `demo_reset` and `metrics_updated` events.
* `GET /demo/snapshot`: Returns a nested JSON snapshot of the active demo state (parcels, hubs, latest route, trust board, metrics, recent events).
* `POST /demo/validate`: Runs non-destructive demo scenario tests and restores the database state.
* `POST /demo/run/main-wow`: Performs the scripted main hackathon sequence in a single request and returns step-by-step outcomes.

### Routing
* `POST /route/next-hop`: Calculates the best next hop for a parcel from its current location using multi-criteria weighted scoring.
* `GET /route/{parcel_id}`: Returns the latest calculated route for the specified parcel.
* `GET /route/decisions`: Returns the history of routing decisions made by the engine.

### Scan Ingest & Validation (ImmuneNet)
* `POST /scan`: Standard scan validation running 6 immune checks (geofence, speed, route graph connectivity, clone scans, cold chain, and tamper checks).
* `POST /scan/fake`: Simulates a fake GPS scan mismatch.
* `POST /scan/clone`: Simulates a parcel appearing in multiple places simultaneously.
* `POST /scan/tamper`: Simulates physically broken seals.

### Trust Score Engine
* `GET /trust/hubs`: Returns trust statuses and scores for all hubs.
* `GET /trust/history/{hub_id}`: Returns trust score updates history for a hub.

### Scenarios & Disruptions (AgentOps)
* `POST /scenario/fail-hub`: Fails a hub completely, forcing reroutes.
* `POST /scenario/overload-hub`: Increases congestion risk.
* `POST /scenario/traffic-jam`: Increases segment travel duration.
* `POST /scenario/weather-risk`: Applies adverse conditions.
* `POST /scenario/temp-breach`: Induces a temperature breach.

### Hardware Ingest
* `POST /hardware/scan`: Direct IoT scanner RFID/BLE ingestion endpoint. If GPS coordinates are missing, returns `requires_gps: true` redirection.
* `POST /hardware/p2p-handshake`: Ingests peer-to-peer handshakes between ESP-NOW nodes.

### Ledger
* `GET /ledger/events`: Lists events ledger (supports limit, event_type, parcel_id, hub_id, and decision query parameters).
* `GET /ledger/parcel/{parcel_id}`: Lists rich ledger timeline for a specific parcel.

---

## WebSocket Events (`/ws`)

Clients connecting to `ws://localhost:8000/ws` receive real-time streams wrapped in standard envelopes (`type`, `timestamp`, `payload`):
* `demo_reset`: Broadcasted when the database is seeded or reset.
* `scan_received`: Broadcasted when a new scan reaches ImmuneNet.
* `movement_accepted`: Broadcasted when a scan passes all checks.
* `movement_blocked`: Broadcasted when threat validation fails.
* `trust_updated`: Broadcasted when trust score updates occur.
* `metrics_updated`: Broadcasted when metrics are updated.
* `route_decision`: Broadcasted when route recalculations are made.
* `hardware_scan_received`: Broadcasted when an IoT scanner initiates a scan.
* `hardware_scan_completed`: Broadcasted when hardware scans finish validation.
* `p2p_handshake`: Broadcasted during ESP-NOW handshakes.

---

## Scripts & CLI Commands

### Smoke Test Script
To run comprehensive health, reset, scanning, scenario, and hardware tests using `curl`:
```bash
bash scripts/smoke_test.sh
```

### Main Demo Simulation Script
To run the full end-to-end hackathon scripted wow sequence:
```bash
bash scripts/demo_run.sh
```

### Run Python Integration Tests
```bash
/tmp/veriroute-backend-venv/bin/python -m pytest tests
```
