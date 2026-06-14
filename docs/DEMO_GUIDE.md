# Demo Guide

Primary objective: prove to judges that this is not a tracking app. It verifies movement claims, blocks impossible events, updates trust, and reroutes dynamically.

## Before Demo

Terminal 1:

```bash
cd backend
source .venv/bin/activate
./run.sh
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Browser:

```text
http://localhost:5173/dashboard
```

Reset:

```bash
curl -X POST http://localhost:8000/demo/reset
```

## 3-Minute Judge Demo Script

| Time | Click path / command | What to say | Expected output |
| --- | --- | --- | --- |
| 0:00 | Open `/dashboard` | "PacketFlow ImmuneNet is TCP/IP for parcels, with an immune system for trust." | Backend live, WebSocket connected, `MED-104` visible. |
| 0:20 | Demo controls: create/seed `MED-104` if needed | "We start with a medicine parcel at HUB-A." | Parcel card and route decision appear. |
| 0:40 | Trigger valid scan | "A movement claim is accepted only after physical plausibility checks." | `ACCEPTED`, green indicator, ledger event. |
| 1:10 | Trigger overload/fail hub | "PacketFlow does not blindly follow fixed routes." | Old route vs new route and reroute event. |
| 1:40 | Trigger fake scan | "ImmuneNet blocks a scan that could not physically be true." | `BLOCKED`, red alert, trust decay. |
| 2:10 | Trigger temp breach | "Cold-chain parcels reroute when the temperature state becomes unsafe." | Temperature breach alert and cold route. |
| 2:40 | Open Ledger/Trust Board | "The proof is auditable: every event is stored and hub trust changes." | Ledger rows, trust scores, event reasons. |
| 2:55 | Close line | "We are not tracking parcels. We are proving movement." | Judges see final concept clearly. |

## 5-Minute Extended Demo Script

1. Dashboard overview: point to PacketFlow decision, ImmuneNet alerts, AgentOps, metrics, and live state.
2. Digital Twin: show hubs, route edges, `MED-104`, and route color changes.
3. Normal scan: submit `HUB-A` scan and show immune check trace.
4. Hardware path: run `hardware_submission/simulation/simulate_hardware.py` or submit `/hardware/scan`.
5. ESP-NOW path: submit `/hardware/p2p-handshake` and show `p2p_handshake`.
6. Hub overload: trigger overload and show route scoring changes.
7. Fake scan: trigger wrong-location scan and show block.
8. Clone/tamper: trigger one extra anomaly and show trust effect.
9. Cold-chain breach: trigger temperature breach and show cold-capable route.
10. Ledger verification: call `/ledger/verify/MED-104` or open ledger page.

## Exact Command Backup Path

```bash
curl -X POST http://localhost:8000/demo/reset
curl -X POST http://localhost:8000/route/next-hop -H "Content-Type: application/json" -d '{"parcel_id":"MED-104","current_hub":"HUB-A","destination_hub":"CUSTOMER-ZONE"}'
curl -X POST http://localhost:8000/scan -H "Content-Type: application/json" -d '{"parcel_id":"MED-104","hub_id":"HUB-A","scanner_id":"SCANNER-07","rfid_verified":true,"qr_verified":true,"gps":{"lat":11.0168,"lng":76.9558,"accuracy_m":18},"temperature_c":24.3,"carrier_type":"van","tamper":false}'
curl -X POST http://localhost:8000/scenario/overload-hub -H "Content-Type: application/json" -d '{"hub_id":"HUB-B","parcel_id":"MED-104","congestion":0.95}'
curl -X POST http://localhost:8000/scan/fake -H "Content-Type: application/json" -d '{"parcel_id":"MED-104","claimed_hub":"HUB-C","fake_gps":{"lat":11.1,"lng":77.1,"accuracy_m":20}}'
curl -X POST http://localhost:8000/scenario/temp-breach -H "Content-Type: application/json" -d '{"parcel_id":"MED-104","hub_id":"HUB-A","temperature_c":29.2}'
curl http://localhost:8000/ledger/events?limit=10
curl http://localhost:8000/trust/hubs
```

## Expected Dashboard Output

- Backend mode shows live when `/health` succeeds.
- WebSocket status should connect after backend is live.
- Route panel should show selected next hop and candidate scores.
- ImmuneNet panel should show blocked fake/clone/tamper/cold-chain events.
- Trust board should show changed hub scores after anomalies.
- Ledger should show `parcel_created`, scans, route decisions, trust updates, scenario events, and hardware events where used.

## Backup Demo Path

| Failure | Backup |
| --- | --- |
| RFID hardware fails | Use QR/manual scan page or `/scan` curl. |
| GPS permission fails | Use demo coordinates in request body. |
| Temperature sensor fails | Use `/scenario/temp-breach`. |
| WebSocket fails | Refresh dashboard; frontend also syncs from `/demo/snapshot`. |
| Frontend fails | Use curl sequence and FastAPI `/docs`. |
| Backend fails | Show README, architecture docs, and recorded video; restart backend with `./run.sh`. |
| Internet fails | Localhost demo uses SQLite and does not need internet after dependencies are installed. |
