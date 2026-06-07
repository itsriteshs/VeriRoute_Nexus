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
