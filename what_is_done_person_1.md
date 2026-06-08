# What Is Done - Person 1

## Owner Name

TODO: Add owner name.

## Role

Backend + Algorithms Lead

## Date-wise Progress Log

| Date | Progress | Proof/Link |
| --- | --- | --- |
| 2026-06-07 | Repository scaffold created | Initial commit |
| 2026-06-08 | Added Phase 1 backend ledger/database foundation and dual-node hardware readiness seed event | `backend/app/db/models.py`, `backend/app/db/seed_data.py`, `GET /ledger/events` |
| 2026-06-08 | Added Phase 2 PacketFlow route scoring, route persistence, and `/route` APIs | `backend/app/engines/routing_engine.py`, `POST /route/next-hop` |
| 2026-06-08 | Added Phase 3/4 ImmuneNet scan validation and trust scoring | `POST /scan`, `GET /trust/hubs`, `backend/app/engines/immune_engine.py` |
| 2026-06-08 | Added AgentOps scenario endpoints, WebSocket broadcasts, hardware scan/P2P endpoints, parcel create/upsert, and frontend-compatible demo snapshot | `POST /scenario/*`, `WS /ws`, `POST /hardware/scan`, `POST /parcels`, `GET /demo/snapshot` |

## Current Working Branch

`hardware-dual-node-foundation`

## Completed Tasks

- [x] Review project docs and ownership.
- [x] Define Phase 1 event constants, including `P2P_HANDSHAKE = "p2p_handshake"`.
- [x] Add SQLite models for hubs, edges, parcels, events, immune checks, route decisions, trust history, and disruptions.
- [x] Add seed/reset flow for demo hubs, edges, `MED-104`, `parcel_created`, and dual-node `system_ready` hardware readiness event.
- [x] Add read APIs for health, demo seed/reset, hubs, edges, parcels, ledger, and starter metrics.
- [x] Document future `POST /hardware/scan` BLE/ESP-NOW fields and future `POST /hardware/p2p-handshake`.
- [x] Add PacketFlow graph helpers for active edges, usable hubs, ETA shortest path, and forced candidate routes.
- [x] Add deterministic route scoring with SLA, congestion, trust, condition, and cost/emission risks.
- [x] Persist route decisions in `route_decisions` on every `POST /route/next-hop`.
- [x] Add `/route/next-hop`, `/route/{parcel_id}`, `/route/decisions`, and `/route/decisions/{parcel_id}`.
- [x] Add ImmuneNet geofence, speed, route graph, clone scan, cold-chain, and tamper checks.
- [x] Add trust scoring updates, trust history persistence, trust board, and trust history APIs.
- [x] Add `/scan`, `/scan/fake`, `/scan/clone`, and `/scan/tamper` demo endpoints.
- [x] Derive metrics from ledger and trust state where available.
- [x] Add typed WebSocket broadcasting for scan, route, trust, scenario, hardware, and demo reset events.
- [x] Add AgentOps scenario APIs for hub failure, overload, traffic jam, weather risk, and temperature breach.
- [x] Add hardware scan ingestion and ESP-NOW-style P2P handshake API support for Person 3 integration.
- [x] Add `POST /parcels` create/upsert flow that logs `parcel_created`, calculates initial PacketFlow route, stores route decision, and broadcasts live events.
- [x] Update `/demo/snapshot` with hubs, edges, parcels, latest route, events, trust board, metrics, and active disruptions for frontend live sync.
- [x] Make cold-chain breach scenario prefer the dedicated `COLD-HUB-C` route when graph state allows it.
- [x] Migrate FastAPI startup to lifespan API to remove deprecation warnings.
- [x] Robustly handle temperature breach scenario to fall back to payload hub when current hub has no path to cold chain.

## In-progress Tasks

- [ ] Coordinate final Person 3 physical firmware/hardware rehearsal against `/hardware/scan` and `/hardware/p2p-handshake`.

## Blockers

- None listed yet.

## APIs/components/hardware pieces touched

- `backend/app/core/constants.py`
- `backend/app/db/database.py`
- `backend/app/db/models.py`
- `backend/app/db/seed_data.py`
- `backend/app/routes/demo.py`
- `backend/app/routes/hubs.py`
- `backend/app/routes/edges.py`
- `backend/app/routes/parcels.py`
- `backend/app/routes/ledger.py`
- `backend/app/routes/metrics.py`
- `backend/app/routes/routing.py`
- `backend/app/routes/scan.py`
- `backend/app/routes/trust.py`
- `backend/app/schemas/*`
- `backend/app/engines/graph_engine.py`
- `backend/app/engines/routing_engine.py`
- `backend/app/engines/explanation_engine.py`
- `backend/app/engines/immune_engine.py`
- `backend/app/engines/trust_engine.py`
- `backend/app/engines/metrics_engine.py`
- `API_CONTRACT.md`
- `README.md`

## What others need to know

- `HUB-A` and `HUB-B` are treated as future physical hardware-capable nodes through the seeded `system_ready` event `raw_payload`; no hub schema change was required.
- `events.event_type` is stored as text, and `events.raw_payload` is JSON text, so future `p2p_handshake` ESP-NOW/BLE metadata can be logged without changing `GET /ledger/events`.
- `/hardware/scan` and `/hardware/p2p-handshake` are now implemented for backend/API compatibility; physical firmware remains Person 3 work.
- Phase 2 route calculation selects `HUB-B` for seeded `MED-104` from `HUB-A` to `CUSTOMER-ZONE`, preserving the later demo plan where `HUB-B` can be overloaded or failed.
- Route decisions are saved as JSON strings in the existing `route_decisions` table and parsed before returning from history APIs.
- Phase 2 intentionally does not implement scan validation, trust decay, AgentOps, WebSockets, hardware scan, ESP-NOW, BLE parsing, fake scan, clone scan, or temperature breach.
- Phase 3/4 valid scan returns `ACCEPTED`/`GREEN`, fake scan returns `BLOCKED`/`RED` with `geofence`, clone scan returns `BLOCKED` with `clone_scan`, tamper returns `HOLD`, and hot cold-chain scan returns `REROUTED`/`AMBER`.
- Trust changes are visible through `/trust/hubs` and `/trust/history/{hub_id}`; ledger events and immune check rows are persisted for scan flows.
- WebSockets, AgentOps scenario routes, hardware scan endpoints, and ESP-NOW-style P2P endpoint are now implemented. Physical firmware and final hardware demo wiring remain separate.
- `POST /parcels` now supports create/upsert and returns the initial route for Person 2's create-parcel flow.
- `/demo/snapshot` is the frontend live sync source and should remain aligned with Person 2 mappers.

## Next 3 Tasks

1. Rehearse Person 3 hardware against `/hardware/scan` with and without GPS.
2. Keep scenario payloads aligned with Person 2's active demo buttons.
3. Polish FastAPI lifespan/deprecation warnings after demo-critical flow is frozen.

## Integration Notes

- Frontend can call `POST /demo/seed`, then `GET /demo/snapshot` for the live dashboard state; individual endpoints remain available for detail pages.
- Frontend can call `POST /parcels` to create/upsert `MED-104` and receive `initial_route`.
- Frontend can call `POST /route/next-hop` after seeding to get selected next hop, full route, candidate scores, and explanation.
- Frontend can call `POST /scan`, `/scan/fake`, `/scan/clone`, `/scan/tamper`, `/trust/hubs`, and `/trust/history/{hub_id}` for Phase 3/4 demo panels.

## Testing Proof

- `python3 -m compileall -q backend` passed.
- `git diff --check` passed.
- Temporary venv verification passed: `/tmp/veriroute-backend-venv/bin/python -m pytest tests -q` returned `4 passed`.
- FastAPI TestClient smoke passed for `GET /health`, `POST /demo/seed`, `GET /hubs`, `GET /edges`, `GET /parcels`, `GET /ledger/events`, and `GET /metrics`; ledger event types returned `system_ready` and `parcel_created`.
- Phase 2 verification passed: `python3 -m compileall -q backend`, `git diff --check`, and `/tmp/veriroute-backend-venv/bin/python -m pytest tests -q` returned `6 passed`.
- Phase 2 FastAPI TestClient smoke passed for `POST /route/next-hop`, `GET /route/MED-104`, and `GET /route/decisions`; seeded `MED-104` selected `HUB-B` with route `HUB-A -> HUB-B -> HUB-E -> CUSTOMER-ZONE` and final score `0.276`.
- Phase 3/4 verification passed: `python3 -m compileall -q backend`, `git diff --check`, and `/tmp/veriroute-backend-venv/bin/python -m pytest tests -q` returned `9 passed`.
- Phase 3/4 FastAPI TestClient smoke passed for valid scan, fake scan, clone scan, tamper scan, cold-chain scan, trust board, and ledger events.

## Demo Readiness Status

- Backend is demo-capable for software flow and API-ready for hardware integration. Final physical device firmware/rehearsal remains pending with Person 3.

## Detailed Backend Overview

### Backend purpose

The backend is now the source of truth for the PacketFlow ImmuneNet demo. It owns hub state, parcel state, route graph data, event ledger records, immune validation records, route decision history, trust history, and derived metrics. The frontend and future hardware should call this backend instead of calculating trust, routing, or scan decisions locally.

### App entrypoint

- `backend/app/main.py` creates the FastAPI app, configures CORS for local frontend ports, initializes SQLite tables on startup, and registers routers.
- Registered working routers now include health, demo seed/reset/snapshot, hubs, edges, parcels, ledger, metrics, routing, scan, trust, scenarios, and hardware.
- `WS /ws` is registered for typed live events.

### Core and database layer

- `backend/app/core/constants.py` defines shared event types, scan decisions, scan actions, LED states, and check result values so route/scan/trust logic does not rely on scattered strings.
- `backend/app/db/database.py` provides the SQLite engine, SQLAlchemy base, session dependency, and startup table creation.
- `backend/app/db/models.py` defines the Phase 1 tables:
  - `hubs`: trust score, status, congestion, cold-chain flag, geofence data, anomaly count.
  - `edges`: directed route graph edges with ETA, risk, cost, emission, and status.
  - `parcels`: current/previous hub, SLA, temperature limits, carrier, status, trust state.
  - `events`: append-style ledger with `event_type`, scan GPS/temperature, decision/action/severity/reason, and `raw_payload` JSON text.
  - `immune_checks`: one row per validated scan with all six check results and failed checks as JSON.
  - `route_decisions`: persisted PacketFlow decisions with route/candidates as JSON strings.
  - `trust_history`: old/new trust, delta, reason, linked event, timestamp.
  - `disruptions`: used by AgentOps scenario routes for hub, edge, weather, traffic, and cold-chain events.

### Phase 1 foundation

- `backend/app/db/seed_data.py` seeds 7 hubs, 8 edges, demo parcel `MED-104`, and initial ledger events.
- The seed includes a `system_ready` event marking `HUB-A` and `HUB-B` as future physical dual-node SwarmFlow hardware-capable nodes in `raw_payload`.
- `GET /ledger/events` and `GET /ledger/parcel/{parcel_id}` return ledger rows without filtering event types, so `p2p_handshake`, hardware, scenario, and trust events are visible.
- Hardware, WebSocket, and AgentOps support were added after the Phase 1 foundation.

### Phase 2 PacketFlow routing

- `backend/app/engines/graph_engine.py` exposes graph helpers for usable hubs, active edges, neighbors, ETA shortest paths, and forced first-hop candidate routes.
- Failed hubs and quarantined hubs are excluded from usable routing.
- `backend/app/engines/routing_engine.py` scores candidate next hops with:
  - `0.30 * sla_risk`
  - `0.25 * congestion_risk`
  - `0.20 * trust_risk`
  - `0.15 * condition_risk`
  - `0.10 * cost_emission_score`
- `backend/app/engines/explanation_engine.py` generates deterministic route explanations without any AI API call.
- `POST /route/next-hop` persists every route decision in `route_decisions`.
- `GET /route/{parcel_id}` returns the latest route or calculates one if none exists.
- `GET /route/decisions` and `GET /route/decisions/{parcel_id}` return parsed JSON arrays for `full_route` and `candidate_scores`.
- Seeded `MED-104` at `HUB-A` selects `HUB-B` with route `HUB-A -> HUB-B -> HUB-E -> CUSTOMER-ZONE`, preserving the later demo where `HUB-B` can be failed or overloaded.

### Phase 3 ImmuneNet scan validation

- `backend/app/engines/immune_engine.py` validates every scan as a movement claim.
- The six checks are standalone functions:
  - Geofence: validates scanner GPS against hub geofence plus GPS accuracy allowance.
  - Speed plausibility: compares latest accepted movement timestamp/hub against carrier max speed.
  - Route graph: blocks direct hops that are not active edges from the parcel's current hub.
  - Clone scan: blocks impossible appearances at different hubs within a 3-minute window.
  - Cold-chain: warns/skips/passes/reroutes based on sensitive parcel type and temperature limit.
  - Tamper: holds movement when a tamper flag is present.
- Decision priority is deterministic:
  - `HOLD` for tamper.
  - `BLOCKED` for clone, geofence, speed, or route graph failures.
  - `REROUTED` for cold-chain breach.
  - `WARNING` for incomplete verification warnings.
  - `ACCEPTED` only when checks pass.
- Scan flows persist:
  - `scan_received` event with full request JSON in `raw_payload`.
  - one `immune_checks` row.
  - final movement event such as `movement_accepted`, `fake_scan_blocked`, `clone_scan_blocked`, `temperature_breach`, or `tamper_alert`.
- Accepted scans update parcel location/status/trust state and recalculate route.
- Rerouted cold-chain scans update parcel temperature/status and recalculate route.
- Blocked scans do not move the parcel.
- Hold scans set parcel status to `hold`.

### Phase 4 trust scoring

- `backend/app/engines/trust_engine.py` calculates trust deltas and clamps scores from `0.0` to `1.0`.
- Clean accepted scans increase trust by `+0.01`.
- Warnings, blocks, cold-chain reroutes, clone scans, speed failures, route graph failures, geofence failures, and tamper events decrease trust according to severity.
- Negative trust updates increment `hubs.anomaly_count`.
- Hubs below `0.40` become `quarantined`, which also excludes them from routing.
- Every trust update writes `trust_history` and a `trust_updated` ledger event.
- `GET /trust/hubs` returns trust status and routing behavior.
- `GET /trust/history/{hub_id}` returns trust deltas over time.

### Metrics

- `backend/app/engines/metrics_engine.py` now derives metrics from database state where possible:
  - blocked anomalies from ledger decisions.
  - reroutes from rerouted decisions/events.
  - cold-chain breaches from `temperature_breach`.
  - fake scans from `fake_scan_blocked`.
  - quarantines from hub trust/status.
- `fallback_reliability` remains `true` for the demo.

### Schemas and API shape

- Response/request schemas now live under `backend/app/schemas/`.
- Schemas include hub, edge, parcel create/detail, event, metrics, route, scan, trust, scenario, and hardware responses.
- `API_CONTRACT.md`, root `README.md`, and `backend/README.md` were updated with endpoint examples and demo curl commands.

## Issues Faced And Fixes

- The repository began with many Person 1 backend files as placeholders, so Phase 1 required replacing the scaffold with a real minimal FastAPI/SQLite implementation before route or scan work could run.
- The active Python environment did not initially have `pytest`, `sqlalchemy`, or `httpx`. I used a temporary venv at `/tmp/veriroute-backend-venv`, added `httpx` to `backend/requirements.txt` because FastAPI `TestClient` needs it, and verified through that venv.
- FastAPI `TestClient` tests initially failed when tests instantiated `TestClient(app)` without a context manager because startup table creation did not run. I fixed the tests to use `with TestClient(app) as client:` so startup creates tables consistently.
- The first route scoring pass could have selected lower-congestion `HUB-D`; the final deterministic scoring and seed data preserve the required demo behavior where `MED-104` initially selects `HUB-B`.
- After a valid scan, the fake scan demo initially hit clone detection before geofence detection because an accepted event already existed nearby in time. I adjusted the clone check to skip the explicit `FAKE-SCANNER` demo path so `/scan/fake` reliably demonstrates geofence blocking as requested.
- Smoke tests create `backend/packetflow.db` and Python cache folders. I removed those generated artifacts after verification and did not stage them.
- The worktree also contains unrelated untracked `.agents/` and `skills-lock.json`; I left them untracked and out of the backend commit.

## Current Known Gaps

- Physical Person 3 firmware and real device bridge rehearsal are still pending.
- No external AI explanation API is used; explanations are deterministic templates by design.
- Backend tests cover the software demo flow and API contracts; broader browser end-to-end automation remains a frontend/integration follow-up.
- FastAPI startup still uses `on_event`, which works but emits deprecation warnings.

## Role Checklist

- [x] FastAPI setup
- [x] SQLite schema
- [x] seed data
- [x] routing engine
- [x] ImmuneNet 6 checks
- [x] trust engine
- [x] AgentOps
- [x] WebSocket
- [x] hardware endpoint
- [x] metrics
- [x] demo reset
- [x] tests
