# Feature Status

| Feature | Status | Evidence | How to demo | Risk | Fix required |
| --- | --- | --- | --- | --- | --- |
| PacketFlow Routing Engine | Implemented and working | `backend/app/engines/routing_engine.py`, `backend/tests/test_routing_engine.py`, `test_routing_phase2.py` | `POST /route/next-hop` | Low | Keep route examples synced with seed data. |
| Route graph and hub data | Implemented and working | `backend/app/db/seed_data.py`, `data/demo_hubs.json`, `data/demo_edges.json` | `GET /hubs`, `GET /edges` | Low | None. |
| Proof-of-Movement scan validation | Implemented and working | `backend/app/engines/immune_engine.py`, `backend/app/routes/scan.py`, tests | `POST /scan` | Low | Add more edge-case tests if time. |
| Geofence check | Implemented and working | `immune_engine.py`, `backend/app/utils/geo.py` | Valid/fake scan | Low | None. |
| Speed plausibility | Implemented but limited | `immune_engine.py` | Rapid sequential scans or clone scenario | Medium | Add explicit demo script for speed-only failure. |
| Route graph validity | Implemented and working | `immune_engine.py`, `backend/app/db/models.py` | Scan invalid hub transition | Low | None. |
| Clone scan blocking | Implemented and working | `/scan/clone`, tests | `POST /scan/clone` | Low | None. |
| Fake scan blocking | Implemented and working | `/scan/fake`, tests | `POST /scan/fake` | Low | None. |
| Tamper hold | Implemented and working | `/scan/tamper`, `immune_engine.py` | `POST /scan/tamper` | Low | None. |
| Cold-chain breach handling | Implemented and working | `/scenario/temp-breach`, `routing_engine.py`, tests | Trigger temperature breach | Low | Keep docs clear that sensor source can be simulated. |
| Hub trust ledger | Implemented and working | `trust_engine.py`, `TrustHistory`, `/trust/*` | `GET /trust/hubs`, fake scan then history | Low | None. |
| Event hash chain | Implemented and working | `Event` hook in `models.py`, `/ledger/verify/{parcel_id}` | Run ledger verification | Medium | Add independent tamper test if time. |
| AgentOps replanner | Implemented and working | `agentops_engine.py`, `/scenario/*`, scenario tests | Trigger fail/overload/traffic/weather | Low | None. |
| SwarmFlow Digital Twin | Implemented but needs final visual QA | `frontend/src/components/twin/*`, pages | Open `/digital-twin` | Medium | Capture screenshots and run browser test. |
| Frontend live state | Implemented and working by design | `usePacketFlowLiveState.ts`, `api/websocket.ts` | Backend live + dashboard | Medium | Browser rehearsal before submission. |
| WebSocket event stream | Implemented and tested | `websocket_manager.py`, `/ws`, tests | Open dashboard or WS client | Low | None. |
| Demo controls | Implemented | `DemoControlsPage.tsx`, `usePacketFlowLiveState.ts` | `/demo-controls` | Medium | Browser QA. |
| Hardware scan bridge | Implemented and working | `/hardware/scan`, `hardware_engine.py`, tests | Simulator or curl | Medium | Show physical proof/video if available. |
| ESP-NOW P2P handshake | Implemented as backend/simulator support | `/hardware/p2p-handshake`, tests | curl or simulator | Medium | Label as hardware-ready unless live hardware shown. |
| BLE Smart Parcel Tag | Partially implemented/hardware-ready | firmware, simulator payload fields | Hardware simulator | Medium | Physical BLE verification video. |
| CAD/PCB assets | Hardware-supported | `hardware_submission/cad`, `hardware_submission/pcb` | Show files/renders | Low | Add screenshots to docs. |
| AI explanation layer | Simulated/demo-only deterministic explanations | `explanation_engine.py` | Route/scan reason strings | Low | Do not claim LLM dependency. |
| Production auth/security | Documented but missing | No auth middleware or device key enforcement | Not demoed | High | Future roadmap; avoid production claim. |
| Frontend automated tests | Documented but missing | `package.json` has no test script | Not demoed | Medium | Add Playwright/Vitest if time. |
