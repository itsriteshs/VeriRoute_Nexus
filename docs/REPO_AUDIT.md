# Repository Audit

Audit date: 2026-06-14  
Project: PacketFlow ImmuneNet, formerly VeriRoute Nexus  
Audit posture: strict Round 1 judge-readiness review based on files present in this checkout.

## Tree Summary

```text
.
├── backend/                 FastAPI backend, engines, schemas, tests, local SQLite files
├── data/                    JSON demo fixtures for hubs, edges, parcels, scenarios
├── docs/                    Architecture, contracts, planning, research, and judge docs
├── frontend/                React/Vite digital twin and dashboard
├── hardware_submission/     ESP32 firmware, simulator, CAD, PCB, wiring, renders
├── presentation/            Demo script, backup plan, Q&A, screenshot checklist
├── scripts/                 Root helper scripts for backend/frontend/reset/seed
├── README.md                Main judge-facing overview
└── what_is_done_person_*.md Team ownership trackers
```

## Major Folders

| Folder | Purpose | Evidence |
| --- | --- | --- |
| `backend/` | FastAPI app for route decisions, scan validation, scenario handling, hardware bridge, metrics, ledger, trust. | `backend/app/main.py`, `backend/app/routes/`, `backend/app/engines/`, `backend/tests/` |
| `frontend/` | Vite/React dashboard with digital twin, demo controls, ledger, parcel pages, scan page, trust board. | `frontend/src/App.tsx`, `frontend/src/pages/`, `frontend/src/components/`, `frontend/src/hooks/usePacketFlowLiveState.ts` |
| `hardware_submission/` | Hardware-ready SmartHub and Smart Parcel Tag package, including firmware, simulator, pin maps, PCB/CAD docs. | `hardware_submission/firmware/`, `hardware_submission/simulation/simulate_hardware.py`, `hardware_submission/diagrams/` |
| `data/` | Deterministic demo graph and scenario fixture files. | `data/demo_hubs.json`, `data/demo_edges.json`, `data/demo_parcels.json`, `data/demo_scenarios.json` |
| `docs/` | Existing architecture/contracts plus this judge-readiness documentation set. | `docs/architecture/`, `docs/contracts/`, top-level docs added in this pass |
| `presentation/` | Demo narrative and backup plans. | `presentation/demo_script.md`, `presentation/backup_demo_plan.md`, `presentation/judge_qna.md` |

## Frontend

Framework: React with Vite and TypeScript.  
Routes/pages found: `/dashboard`, `/digital-twin`, `/parcels`, `/parcels/:parcelId`, `/immunenet`, `/trust-board`, `/demo-controls`, `/ledger`, `/scan/:hubId`.

Key files:

- `frontend/src/App.tsx`: lightweight client-side routing.
- `frontend/src/api/client.ts`: API base URL uses `VITE_API_BASE_URL`, fallback `http://localhost:8000`.
- `frontend/src/api/websocket.ts`: WebSocket URL uses `VITE_WS_URL`, fallback `ws://localhost:8000/ws`.
- `frontend/src/hooks/usePacketFlowLiveState.ts`: fetches snapshot, maps backend data, opens WebSocket, provides demo actions.
- `frontend/src/components/twin/`: digital twin graph rendering.
- `frontend/src/components/dashboard/`: dashboard panels and demo controls.

Weaknesses:

- No automated browser/e2e test suite is present.
- No screenshot assets are currently checked into `docs/screenshots`.
- Frontend has uncommitted changes in digital twin files; judge-doc pass intentionally did not edit them.

## Backend

Framework: FastAPI with SQLAlchemy and SQLite.  
Entrypoint: `backend/app/main.py`.  
Database: SQLAlchemy models in `backend/app/db/models.py`; seed data in `backend/app/db/seed_data.py`.

Modules found:

- `routing_engine.py`: PacketFlow next-hop scoring and persistence.
- `immune_engine.py`: scan validation, anomaly checks, trust update linkage.
- `trust_engine.py`: hub trust score and history.
- `agentops_engine.py`: disruption logging and replanning support.
- `hardware_engine.py`: hardware payload normalization and LED/OLED/buzzer command generation.
- `metrics_engine.py`: demo counters.
- `graph_engine.py`: route graph utilities.
- `explanation_engine.py`: deterministic explanation strings.

## Database And Storage

Tables found in `backend/app/db/models.py`:

- `hubs`
- `edges`
- `parcels`
- `events`
- `immune_checks`
- `route_decisions`
- `trust_history`
- `disruptions`

Ledger support is real in the MVP: `Event` rows compute `prev_hash` and `event_hash` before insert.

## API Routes Found

FastAPI routers expose:

- Health/readiness: `/health`, `/ready`, `/`, `/ws/status`
- Demo: `/demo/seed`, `/demo/reset`, `/demo/snapshot`, `/demo/validate`, `/demo/run/main-wow`, `/demo/toggle-sync`, `/demo/flush-sync`
- Data: `/hubs`, `/edges`, `/parcels`, `/parcels/{parcel_id}`
- Ledger: `/ledger/events`, `/ledger/parcel/{parcel_id}`, `/ledger/verify/{parcel_id}`
- Metrics: `/metrics`
- Routing: `/route/next-hop`, `/route/decisions`, `/route/decisions/{parcel_id}`, `/route/{parcel_id}`
- Scan: `/scan`, `/scan/fake`, `/scan/clone`, `/scan/tamper`
- Trust: `/trust/hubs`, `/trust/history/{hub_id}`
- Scenarios: `/scenario/fail-hub`, `/scenario/overload-hub`, `/scenario/traffic-jam`, `/scenario/weather-risk`, `/scenario/temp-breach`
- Hardware: `/hardware/scan`, `/hardware/p2p-handshake`

## WebSocket/Event Routes

- WebSocket route: `/ws`
- Status route: `/ws/status`
- Event envelope: `{"type":"event_type","timestamp":"...","payload":{...}}`
- Event constants live in `backend/app/core/constants.py`.

## Simulation And Digital Twin Logic

Simulation is deterministic and demo-oriented:

- Seed graph in `backend/app/db/seed_data.py` and `data/*.json`.
- Scenario endpoints mutate hub/edge/parcel state and persist disruptions.
- Frontend digital twin renders mapped hubs, edges, route, events, and alerts.

This is not a physics simulator. It is a logistics protocol scenario simulator.

## Hardware / ESP32 / Scan Integration

Hardware support is meaningful but should be presented carefully:

- Firmware: `hardware_submission/firmware/esp32_smart_hub/esp32_smart_hub.ino`, `hardware_submission/firmware/smart_parcel_tag/smart_parcel_tag.ino`.
- Config template: `hardware_submission/firmware/esp32_smart_hub/config.example.h`.
- Backend bridge: `/hardware/scan` and `/hardware/p2p-handshake`.
- Simulator: `hardware_submission/simulation/simulate_hardware.py`.
- Physical docs/assets: CAD, KiCad PCB, pin maps, wiring plan, rendered images.

## Tests Found

Backend tests:

- `test_health.py`
- `test_routing_engine.py`
- `test_routing_phase2.py`
- `test_scan_trust_phase3_4.py`
- `test_immune_engine.py`
- `test_trust_engine.py`
- `test_demo_flow.py`
- `test_hardware_contract.py`
- `test_hardware_relay.py`
- `test_parcel_create_and_snapshot_contract.py`
- `test_routing_scenarios.py`
- `test_scenarios_websocket.py`
- `test_websocket_events.py`

Frontend commands:

- `npm run typecheck`
- `npm run build`
- No frontend unit/e2e tests are defined in `frontend/package.json`.

## Missing Or Weak Areas

| Area | Weakness | Severity |
| --- | --- | --- |
| Screenshots | No checked-in final screenshot set at top-level docs path. | Important |
| Frontend testing | No unit/e2e test script. | Important |
| Production readiness | No auth, device key management, deployment config, or hosted DB migration path. | Important |
| Hardware proof | Strong artifacts and simulator, but not a guaranteed connected physical demo in repo alone. | Important |
| Docs drift | Old README contained stale phase language; updated in this pass. | Fixed |
| Browser rehearsal | Should be run before final video/submission after frontend uncommitted visual changes settle. | Important |

## Commands Required

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run dev
npm run typecheck
npm run build
```

Demo reset:

```bash
curl -X POST http://localhost:8000/demo/reset
```

Hardware simulator:

```bash
cd hardware_submission/simulation
python3 simulate_hardware.py
```
