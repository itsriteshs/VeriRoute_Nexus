# API Reference

Base URL: `http://localhost:8000`  
WebSocket URL: `ws://localhost:8000/ws`

The backend is FastAPI. Visit `http://localhost:8000/docs` while the backend is running for generated OpenAPI docs.

## REST Endpoints

| Method | Path | Purpose | Success | Common errors |
| --- | --- | --- | --- | --- |
| GET | `/` | Root metadata | project summary | None expected |
| GET | `/health` | Health check | `{"status":"ok"}` | 500 if DB check fails |
| GET | `/ready` | Readiness checks | readiness object | 503 if dependencies unavailable |
| POST | `/demo/seed` | Seed deterministic demo data | seeded summary | 500 on DB failure |
| POST | `/demo/reset` | Reset demo data | seeded summary | 500 on DB failure |
| GET | `/demo/snapshot` | Dashboard state bundle | hubs, edges, parcel, route, events, metrics | 500 on DB failure |
| POST | `/demo/validate` | Validate demo backend state | validation result | 500 on DB failure |
| POST | `/demo/run/main-wow` | Run main scripted demo | summary | 404 if parcel missing |
| POST | `/demo/toggle-sync` | Toggle offline sync simulation | sync state | 500 on DB failure |
| POST | `/demo/flush-sync` | Mark unsynced events synced | flush count | 500 on DB failure |
| GET | `/hubs` | Hub list | `{"hubs":[...]}` | 500 on DB failure |
| GET | `/edges` | Edge list | `{"edges":[...]}` | 500 on DB failure |
| POST | `/parcels` | Create/upsert parcel and initial route | parcel + route | 404/400 if hubs invalid |
| GET | `/parcels` | Parcel list | `{"parcels":[...]}` | 500 on DB failure |
| GET | `/parcels/{parcel_id}` | Parcel details | parcel + events | 404 if missing |
| GET | `/ledger/events` | Event ledger | `{"events":[...]}` | 500 on DB failure |
| GET | `/ledger/parcel/{parcel_id}` | Parcel proof bundle | events, route, trust, checks | empty arrays if no events |
| GET | `/ledger/verify/{parcel_id}` | Hash-chain verification | validity summary | 404/invalid if no ledger |
| GET | `/metrics` | Impact counters | metrics object | 500 on DB failure |
| POST | `/route/next-hop` | Calculate route | route decision | 404 if parcel/hub missing |
| GET | `/route/decisions` | Route history | list | 500 on DB failure |
| GET | `/route/decisions/{parcel_id}` | Parcel route history | list | 500 on DB failure |
| GET | `/route/{parcel_id}` | Latest route | decision object | 404 if no route |
| POST | `/scan` | Validate movement claim | scan decision | 404 if parcel/hub missing |
| POST | `/scan/fake` | Fake scan scenario | blocked scan decision | 404 if parcel missing |
| POST | `/scan/clone` | Clone scan scenario | blocked scan decision | 404 if parcel missing |
| POST | `/scan/tamper` | Tamper scenario | hold decision | 404 if parcel missing |
| GET | `/trust/hubs` | Trust board | hubs with trust status | 500 on DB failure |
| GET | `/trust/history/{hub_id}` | Trust history | history list | empty if none |
| POST | `/scenario/fail-hub` | Hub failure scenario | old/new route | 404 if hub/parcel missing |
| POST | `/scenario/overload-hub` | Hub overload scenario | old/new route | 404 if hub/parcel missing |
| POST | `/scenario/traffic-jam` | Traffic risk scenario | old/new route | 404 if edge/parcel missing |
| POST | `/scenario/weather-risk` | Weather risk scenario | old/new route | 404 if edge/parcel missing |
| POST | `/scenario/temp-breach` | Cold-chain breach scenario | reroute result | 404 if parcel/hub missing |
| POST | `/hardware/scan` | Hardware-native scan bridge | hardware scan decision | 404 if parcel/hub missing |
| POST | `/hardware/p2p-handshake` | ESP-NOW handshake bridge | event id and reason | 404 if parcel/hub missing |
| GET | `/ws/status` | WebSocket status | connection count | None expected |

## Request Examples

Create parcel:

```bash
curl -X POST http://localhost:8000/parcels \
  -H "Content-Type: application/json" \
  -d '{"id":"MED-104","parcel_type":"medicine","source_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE","priority":"high","sla_minutes":45,"temperature_limit":25.0,"carrier_type":"van"}'
```

Valid scan:

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":24.3,"carrier_type":"van","tamper":false}'
```

Route decision:

```bash
curl -X POST http://localhost:8000/route/next-hop \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","current_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE"}'
```

Hardware-native scan payload:

```bash
curl -X POST http://localhost:8000/hardware/scan \
  -H "Content-Type: application/json" \
  -d '{"device_id":"ESP32-HUB-A-01","hub_id":"HUB-A","parcel_id":"MED-104","rfid_uid":"04A8B9C104","qr_payload":"http://localhost:5173/scan/HUB-A?parcel_id=MED-104","temperature_c":24.3,"button_pressed":false,"lat":11.0168,"lng":76.9558,"ble_verified":true,"ble_rssi_m":0.63}'
```

ESP-NOW handshake:

```bash
curl -X POST http://localhost:8000/hardware/p2p-handshake \
  -H "Content-Type: application/json" \
  -d '{"sender_hub":"HUB-A","receiver_hub":"HUB-B","parcel_id":"MED-104","message_type":"TRUST_SYNC","trust_delta":0.02,"eta_sec":300}'
```

Scenario trigger:

```bash
curl -X POST http://localhost:8000/scenario/temp-breach \
  -H "Content-Type: application/json" \
  -d '{"parcel_id":"MED-104","hub_id":"HUB-A","temperature_c":29.2}'
```

## Response Examples

Scan response shape:

```json
{
  "decision": "ACCEPTED",
  "action": "UPDATE_LOCATION",
  "led": "GREEN",
  "parcel_id": "MED-104",
  "hub_id": "HUB-A",
  "immune_checks": {
    "geofence": "PASS",
    "speed": "PASS",
    "route_graph": "PASS",
    "clone_scan": "PASS",
    "cold_chain": "PASS",
    "tamper": "PASS",
    "zero_trust_handshake": "PASS",
    "mesh_consensus": "PASS",
    "statistical_anomaly": "PASS"
  },
  "failed_checks": [],
  "trust_update": {"hub_id": "HUB-A", "old_score": 0.98, "new_score": 0.99, "delta": 0.01},
  "route_decision": {"selected_next_hop": "HUB-B", "full_route": ["HUB-A", "HUB-B", "HUB-E", "CUSTOMER-ZONE"]},
  "reason": "Movement claim accepted."
}
```

Hardware scan response shape:

```json
{
  "status": "processed",
  "accepted": true,
  "decision": "ACCEPTED",
  "action": "UPDATE_LOCATION",
  "led": "GREEN",
  "parcel_id": "MED-104",
  "hub_id": "HUB-A",
  "requires_gps": false,
  "gps_scan_url": null,
  "failed_checks": [],
  "hardware_context": {"scanner_id": "ESP32-HUB-A-01", "rfid_verified": true},
  "reason": "Hardware scan processed through ImmuneNet."
}
```

Error response shape is the standard FastAPI form:

```json
{"detail": "Parcel not found"}
```

## WebSocket Events

Endpoint: `ws://localhost:8000/ws`

Envelope:

```json
{
  "type": "scan_received",
  "timestamp": "2026-06-14T00:00:00Z",
  "payload": {"parcel_id": "MED-104", "hub_id": "HUB-A"}
}
```

Implemented event names:

`parcel_created`, `scan_received`, `movement_accepted`, `movement_blocked`, `movement_warning`, `route_decision`, `reroute_triggered`, `trust_updated`, `temperature_breach`, `fake_scan_blocked`, `clone_scan_blocked`, `tamper_alert`, `hub_failed`, `hub_overloaded`, `traffic_jam`, `weather_risk`, `immune_alert`, `p2p_handshake`, `metrics_updated`, `demo_reset`, `hardware_scan_received`, `hardware_scan_completed`, `ble_tag_detected`, `esp_now_prior_acceptance`.

`simulation_update` is planned/documentation vocabulary, not a separate current constant. Scenario routes emit scenario-specific events.
