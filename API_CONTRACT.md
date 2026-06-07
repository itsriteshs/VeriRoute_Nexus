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
| POST | `/hardware/scan` | Submit Smart Relay Hub scan |
| POST | `/scan/fake` | Inject fake scan scenario |
| POST | `/scan/clone` | Inject clone scan scenario |
| POST | `/scan/tamper` | Inject tamper scenario |
| POST | `/route/next-hop` | Compute next hop |
| GET | `/route/{parcel_id}` | Current route detail |
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

Request:

```json
{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"demo-scanner-1","lat":12.9716,"lng":77.5946,"timestamp":"2026-06-07T10:00:00Z","temperature_c":24.3,"rfid_uid":"RFID-DEMO-104"}
```

Response:

```json
{"accepted":true,"decision":"verified","proof_level":"gps_geofence_identity_sensor","next_hop":"HUB-B","alerts":[],"trust_delta":0.01}
```

## POST /hardware/scan

Request:

```json
{"device_id":"ESP32-HUB-A-01","hub_id":"HUB-A","parcel_id":"MED-104","rfid_uid":"RFID-DEMO-104","qr_payload":"http://localhost:5173/scan/HUB-A?parcel_id=MED-104","temperature_c":24.3,"button_pressed":true,"lat":12.9716,"lng":77.5946,"timestamp":"2026-06-07T10:00:00Z"}
```

Response:

```json
{"accepted":true,"led":"green","decision":"verified","message":"Movement proof accepted for MED-104 at HUB-A"}
```

## POST /scan/fake

Request:

```json
{"parcel_id":"MED-104","claimed_hub_id":"HUB-E","reason":"impossible movement demo"}
```

Response:

```json
{"accepted":false,"decision":"blocked","alerts":["fake_scan","impossible_movement"],"trust_delta":-0.08}
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

Initial event types: `demo.reset`, `parcel.created`, `scan.verified`, `scan.blocked`, `route.updated`, `hub.failed`, `hub.overloaded`, `temperature.breach`, `metrics.updated`.
