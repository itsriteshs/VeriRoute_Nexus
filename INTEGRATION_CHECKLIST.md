# Integration Checklist

## Backend to Frontend Integration

- [ ] `/health` returns 200.
- [ ] `/hubs`, `/edges`, `/parcels`, and `/metrics` match `API_CONTRACT.md`.
- [ ] Scenario endpoints return route and trust updates.
- [ ] Frontend handles backend errors.

## Frontend to Hardware Integration

- [ ] QR label opens scan page with hub and parcel ID.
- [ ] Scan page accepts phone GPS values.
- [ ] UI shows hardware scan accepted/blocked result.

## Hardware to Backend Integration

- [ ] ESP32 payload matches `/hardware/scan`.
- [ ] RFID UID and temperature fields are included.
- [ ] Green LED means accepted.
- [ ] Red LED means blocked or unavailable.

## WebSocket Event Testing

- [ ] Frontend connects to `/ws`.
- [ ] Reset, parcel, scan, route, alert, trust, and metrics events render.
- [ ] Reconnect behavior is graceful.

## Demo Reset Testing

- [ ] Reset clears volatile state.
- [ ] Seed reloads demo graph.
- [ ] `MED-104` can be recreated every run.

## Offline Fallback Testing

- [ ] Frontend can show static demo data.
- [ ] Hardware bridge can print payload when backend is unavailable.
- [ ] Backup video and screenshots are ready.
