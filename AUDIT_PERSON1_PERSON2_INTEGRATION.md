# PacketFlow ImmuneNet / VeriRoute Nexus Audit

Date: 2026-06-08

Scope:
- Source requirements: `person1_zuup.docx`, `person2_zuup.docx`
- Claimed progress: `what_is_done_person_1.md`, `what_is_done_person_2.md`
- Actual code: `backend/`, `frontend/`
- Audit stance: strict backend, frontend, WebSocket, demo-flow, and Person 3 readiness review

## Executive Verdict
The project is substantially beyond the original scaffold and now has a real FastAPI backend, SQLite models, deterministic routing, ImmuneNet checks, trust scoring, AgentOps scenario endpoints, WebSocket broadcasting, hardware scan ingestion, and a React/Vite dashboard with live backend hooks.

However, it is not yet "every tiny Person 1 and Person 2 requirement complete." The most important gaps are:

1. `POST /parcels` is missing, so the required create-parcel flow is not implemented.
2. Live frontend snapshot integration is incomplete because `/demo/snapshot` does not return `edges` and returns route fields under names the frontend does not consume.
3. The live cold-chain button sends `hub_id: HUB-B`, which does not produce the intended `COLD-HUB-C` route. After a prior HUB-B failure it can return `new_route: []`.
4. Person progress trackers are stale and understate what was implemented after the latest main-branch commit.
5. Frontend has a dead invalid import and no real TypeScript type-check command, so Vite build is not enough as a quality gate.
6. Required frontend pages/components are partly present, but the active TS route set still omits scan, ledger, parcel detail, create parcel, traffic/weather, clone, and tamper controls.

## Verification Run

Passed:
- `python3 -m compileall -q backend`
- `/tmp/veriroute-backend-venv/bin/python -m pytest backend/tests -q`
  - Result: `26 passed`
- `npm run build` from `frontend/`
  - Result: Vite production build passed

Independent API probes:
- `GET /health`: 200
- `GET /ready`: 200
- `POST /demo/reset`: 200
- `POST /route/next-hop`: 200, initial route selected `HUB-B`
- `POST /scenario/fail-hub`: 200, rerouted `HUB-A -> HUB-D -> HUB-E -> CUSTOMER-ZONE`
- `POST /scan/fake`: 200, blocked geofence fake scan and reduced HUB-C trust
- `POST /hardware/scan` without GPS: 200, returned `requires_gps: true`
- `POST /parcels`: 405, missing required endpoint

## Backend Audit

### Structure
Status: mostly pass.

The backend has the planned modular structure:
- `backend/app/main.py`
- `backend/app/core/`
- `backend/app/db/`
- `backend/app/schemas/`
- `backend/app/engines/`
- `backend/app/routes/`
- `backend/app/utils/`

Expected engines exist:
- `routing_engine.py`
- `immune_engine.py`
- `trust_engine.py`
- `agentops_engine.py`
- `explanation_engine.py`
- `metrics_engine.py`
- `graph_engine.py`
- `websocket_manager.py`
- `hardware_engine.py`
- `demo_engine.py`

This is not dumped into one file. Separation is good for hackathon review.

### FastAPI App

Status: pass with minor polish.

Working:
- App starts through `backend/app/main.py`.
- CORS includes local frontend ports.
- `GET /health` works.
- `GET /ready` works.
- JSON response shapes are generally frontend-compatible.
- WebSocket route `/ws` exists.

Minor issue:
- `@app.on_event("startup")` raises FastAPI deprecation warnings. It does not break the demo, but should be migrated to lifespan for polish.

### Database

Status: pass.

SQLite models support the required core entities:
- `hubs`
- `edges`
- `parcels`
- `events`
- `immune_checks`
- `route_decisions`
- `trust_history`
- `disruptions`

Required fields are present for trust score, hub status, congestion, cold-chain, parcel temperature limits, current hub, event reason/decision/raw payload, trust history, and route decision history.

### Seed Data

Status: pass.

`POST /demo/reset` restores:
- 7 hubs
- 8 edges
- demo parcel `MED-104`

The seeded network matches the requested route topology, including:
- `HUB-A -> HUB-B`
- `HUB-A -> HUB-D`
- `HUB-B -> HUB-E`
- `HUB-D -> HUB-E`
- `HUB-A -> HUB-C`
- `HUB-C -> COLD-HUB-C`
- `COLD-HUB-C -> HUB-E`
- `HUB-E -> CUSTOMER-ZONE`

### Required Endpoints

Status: partial pass.

Implemented and working:
- `GET /health`
- `GET /ready`
- `POST /demo/reset`
- `POST /demo/seed`
- `GET /hubs`
- `GET /edges`
- `GET /parcels`
- `GET /parcels/{parcel_id}`
- `POST /scan`
- `POST /hardware/scan`
- `POST /hardware/p2p-handshake`
- `POST /scan/fake`
- `POST /scan/clone`
- `POST /scan/tamper`
- `POST /route/next-hop`
- `GET /route/{parcel_id}`
- `GET /route/decisions`
- `GET /route/decisions/{parcel_id}`
- `POST /scenario/fail-hub`
- `POST /scenario/overload-hub`
- `POST /scenario/traffic-jam`
- `POST /scenario/weather-risk`
- `POST /scenario/temp-breach`
- `GET /trust/hubs`
- `GET /trust/history/{hub_id}`
- `GET /ledger/events`
- `GET /ledger/parcel/{parcel_id}`
- `GET /metrics`
- `WS /ws`

Missing:
- `POST /parcels`

This is a high-severity gap because both Person 1 and Person 2 plans require create-parcel as the first demo scene. Current backend returns 405 for `POST /parcels`.

### Routing Engine

Status: pass with caveat.

The route engine uses the required weighted score formula:
- `0.30 * sla_risk`
- `0.25 * congestion_risk`
- `0.20 * trust_risk`
- `0.15 * condition_risk`
- `0.10 * cost_emission_score`

Confirmed initial route:
- Request: `POST /route/next-hop` for `MED-104`, `HUB-A`, `CUSTOMER-ZONE`
- Result: `HUB-A -> HUB-B -> HUB-E -> CUSTOMER-ZONE`
- Selected next hop: `HUB-B`

Confirmed failure reroute:
- After failing `HUB-B`
- Result: `HUB-A -> HUB-D -> HUB-E -> CUSTOMER-ZONE`

Caveat:
- Graph helpers exclude failed hubs and hubs below trust `0.40`.
- Carrier-incompatible edge exclusion is not implemented even though `allowed_carriers` exists on edges. The prompt says "if implemented," so this is not a hard failure, but it should be called out if judges ask about carrier compatibility.

### ImmuneNet Engine

Status: pass.

All six checks exist:
- geofence
- speed
- route graph
- clone scan
- cold-chain
- tamper

Confirmed fake scan:
- Decision: `BLOCKED`
- Failed checks: `["geofence"]`
- Action: `QUARANTINE_MOVEMENT_CLAIM`
- LED: `RED`
- HUB-C trust: `0.65 -> 0.50`

Expected persistence exists:
- `scan_received`
- `immune_checks`
- final event such as `fake_scan_blocked`, `clone_scan_blocked`, `temperature_breach`, or `tamper_alert`
- `trust_updated`

### Trust Engine

Status: pass.

Trust bands match the plan:
- `>= 0.80`: trusted
- `>= 0.60`: watch
- `>= 0.40`: risky
- `< 0.40`: quarantined

Trust history is stored, clean accepted scans increase trust, blocked scans reduce trust, and quarantined hubs are excluded from routing through the graph helper.

### AgentOps and Scenarios

Status: partial pass.

Working:
- fail hub
- overload hub
- traffic jam
- weather risk
- temperature breach

Each scenario logs a disruption, records events, calls routing, and broadcasts WebSocket updates.

High-risk issue:
- `/scenario/temp-breach` sets `parcel.current_hub = payload.hub_id` before routing.
- When the frontend sends `hub_id: HUB-B`, the new route is `HUB-B -> HUB-E -> CUSTOMER-ZONE`, not the intended `HUB-A -> HUB-C -> COLD-HUB-C -> HUB-E -> CUSTOMER-ZONE`.
- If HUB-B was failed earlier in the demo, the same endpoint can return `new_route: []`.

This undermines the planned cold-chain wow moment unless the UI sends `HUB-A`, the backend forces a cold-hub route, or the demo sequence resets before cold-chain.

### Metrics

Status: pass for demo metrics.

`GET /metrics` returns:
- `scan_validation_latency_ms`
- `reroute_time_ms`
- `anomalies_blocked`
- `reroutes_triggered`
- `cold_chain_breaches`
- `fake_scans_blocked`
- `trust_quarantines`
- `hardware_scans`
- `p2p_handshakes`
- `accepted_movements`
- `ledger_events`
- `fallback_reliability`

The latency and reroute-time values are deterministic demo values, not measured timings. That is acceptable for a hackathon demo if described honestly.

### WebSocket

Status: pass.

`WS /ws` exists and sends structured envelopes:

```json
{
  "type": "event_type_here",
  "timestamp": "...",
  "payload": {}
}
```

Broadcast event types include the required core list:
- `scan_received`
- `movement_accepted`
- `immune_alert`
- `route_decision`
- `reroute_triggered`
- `trust_updated`
- `hub_failed`
- `hub_overloaded`
- `temperature_breach`
- `metrics_updated`
- `demo_reset`

Additional useful hardware events exist:
- `hardware_scan_received`
- `hardware_scan_completed`
- `p2p_handshake`
- `ble_tag_detected`
- `esp_now_prior_acceptance`

### Hardware Readiness

Status: pass.

`POST /hardware/scan` supports:
- `parcel_id`
- `hub_id`
- `scanner_id`
- `rfid_verified`
- `temperature_c`
- `tamper`

It also accepts optional upgraded fields:
- BLE verification
- BLE RSSI
- ESP-NOW prior acceptance
- ESP-NOW prior hub
- ESP-NOW trust delta

Without GPS it returns a phone-GPS continuation response. With GPS it routes through full scan validation and returns LED decision data. `POST /hardware/p2p-handshake` is implemented.

## Frontend Audit

### Structure

Status: mixed pass.

Strong points:
- The active app uses TSX routes and a shared live state hook.
- Expected component families mostly exist under `components/twin`, `components/panels`, `components/alerts`, `components/trust`, `components/ledger`, `components/metrics`, and `components/demo`.
- Backend API client, endpoint definitions, mappers, and WebSocket files exist.

Risks:
- There are old JSX dashboard/page/component files and newer TSX files side by side. Some old files are not in the active route tree.
- Active `App.tsx` only routes:
  - `/dashboard`
  - `/digital-twin`
  - `/parcels`
  - `/immunenet`
  - `/trust-board`
  - `/demo-controls`
- Existing JSX pages such as `ScanPage.jsx`, `LedgerPage.jsx`, and `ParcelDetails.jsx` are not wired into the active TS route set.

### Startup and Build

Status: pass with test gap.

`npm run build` passes.

Gap:
- There is no real `tsc --noEmit` type-check script.
- `frontend/src/api/mappers.ts` imports `get_trust_status` from `./endpoints`, but `endpoints.ts` does not export it. The build survives because the import is unused, but this is sloppy and would fail stricter type/lint checks.

### Dashboard and Live Backend Integration

Status: partial pass.

The live hook attempts:
- health check
- WebSocket connection
- `/demo/snapshot` sync
- polling fallback when WS is disconnected
- live action calls for scan, handshake, fake scan, fail hub, overload hub, temp breach, reset

High-risk integration gap:
- `usePacketFlowLiveState.ts` expects `snapshot.edges`, but `/demo/snapshot` does not return `edges`.
- The same hook maps `snapshot.latest_route.full_route` and `snapshot.latest_route.reason`, but the backend snapshot uses `current_route` and `latest_reason`.
- It expects `candidate_scores`, but snapshot omits it.

Result:
- Backend-live graph edges can be empty.
- Live route reason can be blank.
- Candidate scores can fall back to mock/default values.
- The frontend may appear more integrated than it really is.

### Demo Controls

Status: partial pass.

Active controls:
- Accept Scan
- Trigger ESP-NOW Handshake
- Fail HUB-B
- Overload HUB-B
- Inject Fake Scan
- Raise Temperature
- Reset Demo

Missing from the required Person 2 scenario list:
- Create MED-104
- Trigger Clone Scan
- Trigger Tamper
- Inject Traffic Jam
- Inject Weather Risk

This matters because the backend implements many of these, but the active frontend does not expose them in the judge operator console.

### Scan Page, Ledger Page, Parcel Details

Status: partial.

Files exist:
- `ScanPage.jsx`
- `LedgerPage.jsx`
- `ParcelDetails.jsx`

But they are not wired into the active `App.tsx` route map, so they are not part of the current product flow. This does not satisfy the Person 2 plan as delivered.

### WebSocket Frontend Handling

Status: partial pass.

The frontend does connect to WS in live mode and syncs backend on every event. This is robust as a fallback strategy, but it does not use the event payload to update state directly. That is acceptable for hackathon reliability, but not the full "every event causes direct visible dashboard change" contract unless `/demo/snapshot` is complete and correct.

## Person 3 Readiness

Status: backend ready, frontend partial.

Backend:
- Hardware scan endpoint exists.
- GPS-required fallback exists.
- BLE and ESP-NOW fields are accepted.
- P2P handshake endpoint exists.
- Hardware events enter ledger and WS.
- LED response exists when full GPS validation is available.

Frontend:
- Movement proof panel exists.
- Hardware/P2P controls partially exist.
- Scan page exists but is not wired into active routing.
- There is no active QR/GPS phone flow in the current TS app.

## Progress Tracker Drift

`what_is_done_person_1.md` is stale:
- It says WebSocket, AgentOps, hardware endpoints, and scenarios remain future work.
- The current backend implements those areas and has tests for them.

`what_is_done_person_2.md` is stale:
- It says backend integration and WebSocket remain future work.
- The current frontend has live backend API and WebSocket hooks.

These files should be updated before submission because judges or teammates using them will get the wrong status.

## Highest Priority Fixes

1. Implement `POST /parcels`.
   - Create a parcel.
   - Persist `parcel_created`.
   - Calculate and persist initial route.
   - Broadcast `parcel_created` and `route_decision`.
   - Return `{ parcel, initial_route }`.

2. Fix `/demo/snapshot` to return frontend-compatible live data.
   - Add `edges`.
   - Return `latest_route.full_route`, `latest_route.candidate_scores`, `latest_route.reason`, `latest_route.created_at`.
   - Keep old aliases only if needed.

3. Fix cold-chain demo behavior.
   - Either make frontend send `hub_id: HUB-A` for the intended COLD-HUB-C path, or teach backend `/scenario/temp-breach` to explicitly route toward `COLD-HUB-C`.
   - Guard against running temperature breach after failing HUB-B without a reset.

4. Wire active frontend routes for scan, ledger, and parcel detail.
   - Add `/scan/:hubId`, `/ledger`, and `/parcels/:parcelId` or document intentionally reduced scope.

5. Add missing demo buttons in the active TS controls.
   - Create MED-104
   - Traffic jam
   - Weather risk
   - Clone scan
   - Tamper

6. Clean frontend type quality.
   - Remove invalid `get_trust_status` import.
   - Add TypeScript config and `npm run typecheck`.

7. Update `what_is_done_person_1.md` and `what_is_done_person_2.md`.
   - Bring them in line with the latest backend/frontend integration commit.

## Submission Readiness

Backend: close to demo-ready, with one high-severity missing endpoint and one cold-chain demo hazard.

Frontend: visually and structurally strong, but live integration is not fully trustworthy until snapshot shape, route wiring, and missing controls are fixed.

Person 3 readiness: backend is genuinely ready for hardware integration; frontend still needs the active scan/GPS route wired into the current TS app.
