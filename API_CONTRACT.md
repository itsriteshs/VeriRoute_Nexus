# API Contract

All implementation changes must keep this file current before code changes land. Base URL: `http://localhost:8000`. Frontend URL: `http://localhost:5173`.

## Endpoint Summary

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service health check |
| POST | `/demo/seed` | Load demo graph, parcels, scenarios |
| POST | `/demo/reset` | Reset volatile demo state |
| GET | `/hubs` | List hubs and trust state |
| GET | `/edges` | List route graph edges |
| POST | `/parcels` | Create a parcel |
| GET | `/parcels` | List parcels |
| GET | `/parcels/{parcel_id}` | Parcel detail |
| POST | `/scan` | Submit verified scan |
| POST | `/scan/fake` | Inject fake scan scenario |
| POST | `/scan/clone` | Inject clone scan scenario |
| POST | `/scan/tamper` | Inject tamper scenario |
| POST | `/hardware/scan` | Future phase: submit Smart Relay Hub scan |
| POST | `/route/next-hop` | Compute next hop |
| GET | `/route/{parcel_id}` | Current route detail |
| GET | `/route/decisions` | Latest route decisions |
| GET | `/route/decisions/{parcel_id}` | Route decision history for parcel |
| POST | `/scenario/fail-hub` | Mark hub failed |
| POST | `/scenario/overload-hub` | Mark hub overloaded |
| POST | `/scenario/traffic-jam` | Add traffic risk |
| POST | `/scenario/weather-risk` | Add weather risk |
| POST | `/scenario/temp-breach` | Add cold-chain breach |
| GET | `/trust/hubs` | Hub trust board |
| GET | `/trust/history/{hub_id}` | Hub trust timeline |
| GET | `/ledger/events` | Global event ledger |
| GET | `/ledger/parcel/{parcel_id}` | Parcel ledger |
| GET | `/metrics` | Demo impact metrics |
| WS | `/ws` | Live events for frontend |

## POST /parcels

Request:

```json
{"parcel_id":"MED-104","type":"medicine","source":"HUB-A","destination":"CUSTOMER-ZONE","priority":"high","sla_minutes":45,"temperature_limit_c":25,"carrier":"van"}
```

Response:

```json
{"parcel_id":"MED-104","status":"created","current_hub":"HUB-A","recommended_next_hop":"HUB-B","trust_score":0.92}
```

## POST /scan

Phase 3/4 ImmuneNet scan validation and trust scoring. This endpoint validates a movement claim, writes ledger and immune check rows, updates hub trust, and recalculates a route for accepted or rerouted scans. It does not broadcast WebSockets, call AI APIs, execute AgentOps scenarios, or use hardware endpoints.

Request:

```json
{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":24.3,"carrier_type":"van","tamper":false}
```

Response:

```json
{"decision":"ACCEPTED","action":"UPDATE_LOCATION","led":"GREEN","parcel_id":"MED-104","hub_id":"HUB-A","immune_checks":{"geofence":"PASS","speed":"PASS","route_graph":"PASS","clone_scan":"PASS","cold_chain":"PASS","tamper":"PASS"},"failed_checks":[],"trust_update":{"hub_id":"HUB-A","old_score":0.98,"new_score":0.99,"delta":0.01},"route_decision":{"selected_next_hop":"HUB-B","full_route":["HUB-A","HUB-B","HUB-E","CUSTOMER-ZONE"]},"reason":"Movement accepted because identity, GPS geofence, route validity, speed plausibility, temperature, and tamper checks passed."}
```

Hot cold-chain scan:

```json
{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":29.2,"carrier_type":"van","tamper":false}
```

Expected summary: `decision = REROUTED`, `action = REROUTE_TO_COLD_HUB`, `led = AMBER`, `failed_checks = ["cold_chain"]`.

## POST /route/next-hop

Phase 2 PacketFlow routing only. This endpoint calculates and persists a route decision. It does not mutate parcel trust, validate scans, trigger AgentOps, broadcast WebSockets, or call hardware.

Request:

```json
{"parcel_id":"MED-104","current_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE"}
```

Response:

```json
{"parcel_id":"MED-104","current_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE","selected_next_hop":"HUB-B","full_route":["HUB-A","HUB-B","HUB-E","CUSTOMER-ZONE"],"total_eta_min":35.0,"final_score":0.276,"candidate_scores":[{"hub_id":"HUB-B","full_route":["HUB-A","HUB-B","HUB-E","CUSTOMER-ZONE"],"total_eta_min":35.0,"sla_risk":0.3,"congestion_risk":0.5,"trust_risk":0.08,"condition_risk":0.1,"cost_emission_score":0.3,"final_score":0.276,"selected":true,"rejection_reason":null}],"reason":"HUB-B selected because it gives MED-104 an SLA-safe route while maintaining high hub trust and cold-chain-safe continuation."}
```

PacketFlow final score:

```text
0.30 * sla_risk + 0.25 * congestion_risk + 0.20 * trust_risk + 0.15 * condition_risk + 0.10 * cost_emission_score
```

Error responses:

```json
{"detail":"Parcel not found"}
```

```json
{"detail":"Current hub not found"}
```

```json
{"detail":"Destination hub not found"}
```

No valid route returns HTTP 200 with `selected_next_hop: null`, `full_route: []`, `candidate_scores: []`, and reason `No valid route available from current hub to destination.`

## GET /route/{parcel_id}

Returns the latest route decision, calculating one from the parcel state if no decision exists.

```json
{"parcel_id":"MED-104","current_route":["HUB-A","HUB-B","HUB-E","CUSTOMER-ZONE"],"selected_next_hop":"HUB-B","latest_reason":"HUB-B selected because it gives MED-104 an SLA-safe route while maintaining high hub trust and cold-chain-safe continuation."}
```

## GET /route/decisions

Returns the latest 50 route decisions ordered newest first. `full_route` and `candidate_scores` are parsed JSON arrays.

## POST /hardware/scan

Future phase only. Do not implement this endpoint in Phase 1.

Request:

```json
{"device_id":"ESP32-HUB-A-01","hub_id":"HUB-A","parcel_id":"MED-104","rfid_uid":"RFID-DEMO-104","qr_payload":"http://localhost:5173/scan/HUB-A?parcel_id=MED-104","temperature_c":24.3,"button_pressed":true,"lat":12.9716,"lng":77.5946,"timestamp":"2026-06-07T10:00:00Z","ble_verified":true,"ble_rssi_m":2.4,"esp_now_prior_acceptance":true,"esp_now_prior_hub":"HUB-A","esp_now_trust_delta":0.02}
```

Response:

```json
{"accepted":true,"led":"green","decision":"verified","message":"Movement proof accepted for MED-104 at HUB-A"}
```

## Future POST /hardware/p2p-handshake

Future phase only. This endpoint will later log `p2p_handshake` events between physical `HUB-A` and `HUB-B` SmartHub nodes. Expected ESP-NOW metadata may include `sender_hub`, `receiver_hub`, `parcel_id`, `message_type`, and `trust_delta`; BLE parcel tag metadata may include `parcel_id`, `temperature_c`, `tamper`, and RSSI/proximity estimates.

## GET /ledger/events

Response:

```json
{"events":[{"id":2,"event_type":"system_ready","parcel_id":null,"hub_id":null,"timestamp":"2026-06-08T10:00:00+00:00","gps_lat":null,"gps_lng":null,"gps_accuracy_m":null,"temperature_c":null,"decision":"READY","action":"DUAL_NODE_HARDWARE_READY","severity":"info","reason":"Demo seeded with HUB-A and HUB-B prepared for upgraded dual-node SwarmFlow relay integration.","raw_payload":"{\"hardware_mode\":\"dual_node_swarmflow\",\"physical_nodes\":[\"HUB-A\",\"HUB-B\"],\"future_protocols\":[\"BLE parcel tag\",\"ESP-NOW p2p_handshake\"]}"}]}
```

The `event_type` field is not enum-filtered by the read API. Future `p2p_handshake` rows will be returned by `GET /ledger/events` without route code changes.

## POST /scan/fake

Request:

```json
{"parcel_id":"MED-104","claimed_hub":"HUB-C","fake_gps":{"lat":11.1000,"lng":77.1000,"accuracy_m":20}}
```

Response:

```json
{"decision":"BLOCKED","action":"QUARANTINE_MOVEMENT_CLAIM","led":"RED","failed_checks":["geofence"]}
```

## POST /scan/clone

Request:

```json
{"parcel_id":"MED-104","first_hub":"HUB-B","second_hub":"HUB-D"}
```

Expected summary: `decision = BLOCKED`, `led = RED`, `failed_checks = ["clone_scan"]`.

## POST /scan/tamper

Request:

```json
{"parcel_id":"MED-104","hub_id":"HUB-C","tamper":true}
```

Expected summary: `decision = HOLD`, `action = ALERT_AND_HOLD`, `led = RED`, `failed_checks = ["tamper"]`.

## GET /trust/hubs

Response:

```json
{"hubs":[{"hub_id":"HUB-A","name":"Central Smart Hub A","trust_score":0.99,"trust_status":"trusted","anomaly_count":0,"routing_behavior":"normal","status":"active"}]}
```

## GET /trust/history/{hub_id}

Response:

```json
{"hub_id":"HUB-C","history":[{"old_score":0.65,"new_score":0.5,"delta":-0.15,"reason":"Scan blocked because scanner GPS was outside HUB-C geofence.","event_id":3,"timestamp":"2026-06-08T10:00:00+00:00"}]}
```

## POST /scenario/fail-hub

Request:

```json
{"hub_id":"HUB-B","reason":"demo disruption"}
```

Response:

```json
{"scenario":"fail_hub","hub_id":"HUB-B","status":"failed","affected_routes":["MED-104"],"agentops_action":"reroute_requested"}
```

## POST /scenario/temp-breach

Request:

```json
{"parcel_id":"MED-104","hub_id":"HUB-A","temperature_c":29.2}
```

Response:

```json
{"scenario":"temp_breach","parcel_id":"MED-104","accepted":false,"alerts":["cold_chain_breach"],"agentops_action":"reroute_to_cold_chain","next_hop":"HUB-C"}
```

## GET /metrics

Response:

```json
{"parcels_verified":1,"bad_scans_blocked":1,"reroutes_triggered":2,"avg_trust_score":0.89,"estimated_delay_minutes_saved":18,"cold_chain_breaches_prevented":1}
```

## WS /ws

Event envelope:

```json
{"type":"scan.verified","timestamp":"2026-06-07T10:00:00Z","payload":{"parcel_id":"MED-104","hub_id":"HUB-A","next_hop":"HUB-B","trust_score":0.93}}
```

Initial event constants: `parcel_created`, `scan_received`, `movement_accepted`, `movement_blocked`, `route_decision`, `reroute_triggered`, `trust_updated`, `temperature_breach`, `fake_scan_blocked`, `clone_scan_blocked`, `tamper_alert`, `hub_failed`, `hub_overloaded`, `p2p_handshake`, `metrics_updated`, `demo_reset`.
