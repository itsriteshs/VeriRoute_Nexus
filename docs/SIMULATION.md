# Simulation

PacketFlow ImmuneNet uses a deterministic logistics scenario simulation, not a continuous physics simulator.

## Model

The simulated world is a hub graph:

- Nodes: logistics hubs with GPS coordinates, geofence radius, trust score, congestion, cold-chain ability, status.
- Edges: directed routes with distance, ETA, traffic risk, weather risk, cost score, emission score, carrier allowances.
- Parcel: `MED-104`, a medicine parcel with SLA, temperature limit, carrier type, and current hub.
- Events: scans, route decisions, disruptions, trust updates, hardware messages.

## Hub Graph

Seeded hubs are defined in `backend/app/db/seed_data.py`:

- `HUB-A`: source smart hub.
- `HUB-B`: primary relay.
- `HUB-C`: lower-trust relay.
- `COLD-HUB-C`: dedicated cold-chain hub.
- `HUB-D`: alternate relay.
- `HUB-E`: final relay with cold-chain support.
- `CUSTOMER-ZONE`: destination.

Edges include primary, alternate, and cold-chain paths.

## Parcel Movement Model

A parcel moves only when a scan is accepted. Scan validation checks whether the movement claim is plausible. Accepted scans update parcel location and trigger route recalculation. Blocked or held scans record proof but do not blindly advance the parcel.

## Carrier Types

Carrier type is represented as a string. Current speed plausibility supports values such as `van`, `bike`, `drone`, and `bot` in `immune_engine.py`.

## Scenario Library

| Scenario | Endpoint | Behavior |
| --- | --- | --- |
| Fake scan | `/scan/fake` | Uses wrong GPS/geofence to produce a blocked movement claim. |
| Clone scan | `/scan/clone` | Creates conflicting movement evidence and blocks clone behavior. |
| Tamper | `/scan/tamper` | Forces hold/alert behavior. |
| Hub failure | `/scenario/fail-hub` | Marks hub unavailable and replans. |
| Hub overload | `/scenario/overload-hub` | Raises congestion and replans. |
| Traffic jam | `/scenario/traffic-jam` | Raises edge traffic risk and replans. |
| Weather risk | `/scenario/weather-risk` | Raises edge weather/condition risk and replans. |
| Temperature breach | `/scenario/temp-breach` | Records cold-chain breach and prefers cold-capable routing. |
| Hardware scan | `/hardware/scan` | Normalizes ESP32/native payload and runs scan validation. |
| P2P handshake | `/hardware/p2p-handshake` | Logs inter-hub relay trust message. |

## Deterministic Vs Mocked

| Deterministic | Mocked/demo-only |
| --- | --- |
| Route score formula, geofence checks, route graph checks, trust updates, event persistence, hash-chain generation, WebSocket event envelopes. | Traffic/weather event source, physical parcel motion, live GPS hardware unless connected, real carrier integrations, production identity. |

## Digital Twin

The React digital twin maps backend hubs, edges, parcel state, route decisions, trust, and alerts into a visual logistics graph. It is a dashboard representation of backend state, not an independent simulation engine.
