# Architecture

PacketFlow ImmuneNet has four MVP layers:

1. **Interaction layer:** React/Vite dashboard, scan page, demo controls, hardware simulator.
2. **Protocol API layer:** FastAPI routes for scans, routes, scenarios, trust, ledger, hardware, metrics, and live WebSocket events.
3. **Decision layer:** PacketFlow routing, ImmuneNet validation, AgentOps replanning, trust engine, metrics engine.
4. **State/proof layer:** SQLite/SQLAlchemy models for hubs, edges, parcels, events, immune checks, route decisions, trust history, and disruptions.

## High-Level Diagram

```mermaid
flowchart TB
  subgraph UI[Frontend]
    Dash[Dashboard]
    Twin[Digital Twin]
    Scan[Scan Page]
    Demo[Demo Controls]
    Ledger[Ledger / Trust Board]
  end

  subgraph API[FastAPI Backend]
    Routes[Route Modules]
    WS[WebSocket Manager]
    Packet[PacketFlow Routing]
    Immune[ImmuneNet Validation]
    Agent[AgentOps Scenarios]
    Trust[Trust Engine]
    Metrics[Metrics Engine]
  end

  subgraph Storage[SQLite State]
    Hubs[(Hubs)]
    Edges[(Edges)]
    Parcels[(Parcels)]
    Events[(Events + Hash Chain)]
    Checks[(Immune Checks)]
    Decisions[(Route Decisions)]
    History[(Trust History)]
  end

  subgraph Hardware[Hardware-Ready Layer]
    ESP32[SmartHub ESP32]
    Tag[Smart Parcel Tag]
    Sim[Python Hardware Simulator]
  end

  UI --> Routes
  ESP32 --> Routes
  Tag --> ESP32
  Sim --> Routes
  Routes --> Packet
  Routes --> Immune
  Routes --> Agent
  Immune --> Trust
  Packet --> Decisions
  Trust --> History
  Routes --> Events
  Routes --> WS
  WS --> UI
  Routes --> Storage
```

## Backend Module Architecture

| Module | Role |
| --- | --- |
| `backend/app/main.py` | App creation, CORS, router registration, `/ws`, `/ws/status`, root route. |
| `backend/app/routes/*.py` | API route boundaries for demo, scans, scenarios, hardware, metrics, parcels, routing, trust, ledger, hubs, edges. |
| `backend/app/schemas/*.py` | Pydantic request/response contracts. |
| `backend/app/db/models.py` | SQLAlchemy tables and event hash-chain hook. |
| `backend/app/db/seed_data.py` | Deterministic demo graph and `MED-104` seed. |
| `backend/app/engines/routing_engine.py` | PacketFlow scoring and route decision persistence. |
| `backend/app/engines/immune_engine.py` | Movement claim validation and anomaly outcomes. |
| `backend/app/engines/trust_engine.py` | Trust score and history updates. |
| `backend/app/engines/agentops_engine.py` | Disruption logging and reroute helpers. |
| `backend/app/engines/hardware_engine.py` | Hardware payload normalization and actuator command generation. |
| `backend/app/core/websocket_manager.py` | Live event connection manager and event envelope broadcast. |

## Frontend Component Architecture

| Area | Files |
| --- | --- |
| App shell/routing | `frontend/src/App.tsx`, `components/layout/*` |
| API | `frontend/src/api/client.ts`, `endpoints.ts`, `websocket.ts`, `mappers.ts` |
| State | `hooks/usePacketFlowLiveState.ts`, `usePacketFlowSocket.ts`, `useDemoState.ts` |
| Pages | `pages/Dashboard.tsx`, `DigitalTwinPage.tsx`, `ParcelsPage.tsx`, `ImmuneNetPage.tsx`, `TrustBoardPage.tsx`, `DemoControlsPage.tsx`, `LedgerPage.tsx`, `ScanPage.tsx` |
| Digital twin | `components/twin/*` |
| Dashboard panels | `components/dashboard/*`, `components/panels/*` |
| Ledger/trust | `components/ledger/*`, `components/trust/*` |

## Data Flow

```mermaid
sequenceDiagram
  participant User
  participant UI as React Dashboard
  participant API as FastAPI
  participant Immune as ImmuneNet
  participant Route as PacketFlow
  participant DB as SQLite Ledger
  participant WS as WebSocket

  User->>UI: Click scan/demo action
  UI->>API: POST /scan or /scenario/*
  API->>Immune: validate movement claim
  Immune->>DB: store event + immune check
  Immune->>DB: update trust history
  API->>Route: recalculate next hop
  Route->>DB: persist route decision
  API->>WS: broadcast event envelope
  WS->>UI: live update
  UI->>API: GET /demo/snapshot
  API->>UI: dashboard state
```

## WebSocket/Event Flow

All live messages use:

```json
{
  "type": "route_decision",
  "timestamp": "2026-06-14T00:00:00Z",
  "payload": {}
}
```

Events are emitted by scan processing, scenario routes, hardware routes, demo reset/seed, trust changes, and metric changes. The frontend treats WebSocket events as invalidation signals and refreshes `/demo/snapshot`.

## Database / Ledger Model

`Event` is the proof ledger. Each insert computes:

- `prev_hash`: previous event hash for the same parcel or `GENESIS`.
- `event_hash`: SHA256 over event type, parcel, hub, timestamp, payload, and previous hash.

The ledger is supported by:

- `ImmuneCheck`: detailed check statuses.
- `RouteDecision`: candidate score history and chosen next hop.
- `TrustHistory`: score deltas and reasons.
- `Disruption`: AgentOps scenario records.

## Real Vs Simulated Boundaries

| Real | Simulated |
| --- | --- |
| FastAPI routes, SQLite persistence, route scoring, anomaly checks, trust updates, ledger hashes, WebSocket broadcasts. | Hub graph environment, traffic/weather disruptions, digital twin positions, demo parcel state, hardware simulator interactions. |

Hardware is **hardware-ready**: firmware, payload contracts, simulator, PCB/CAD, and backend bridge exist, but the repo alone cannot prove a currently connected physical ESP32 demo.
