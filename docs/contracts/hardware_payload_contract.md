# Hardware Payload Contract

Post Smart Relay Hub payloads to `POST /hardware/scan`.

The backend accepts both the typed backend shape and the device-native shape used by `hardware_submission/firmware/esp32_smart_hub/esp32_smart_hub.ino` and `hardware_submission/simulation/simulate_hardware.py`.

## Device-native request

```json
{
  "device_id": "ESP32-HUB-A-01",
  "hub_id": "HUB-A",
  "parcel_id": "MED-104",
  "rfid_uid": "RFID4A8B9C104",
  "qr_payload": "http://localhost:5173/scan/HUB-A?parcel_id=MED-104",
  "temperature_c": 24.3,
  "button_pressed": false,
  "lat": 11.0168,
  "lng": 76.9558,
  "timestamp": "2026-06-08T15:00:00Z",
  "ble_verified": true,
  "ble_rssi_m": 1.2,
  "esp_now_prior_acceptance": false,
  "esp_now_prior_hub": "",
  "esp_now_trust_delta": 0.0
}
```

`device_id` maps to backend `scanner_id`, `button_pressed` maps to `tamper`, and flat `lat`/`lng` maps to the backend `gps` object.

## No-GPS handoff

If the hub cannot send GPS, omit `lat` and `lng`. The backend records the hardware scan and returns a phone scan URL:

```json
{
  "status": "hardware_scan_received",
  "accepted": false,
  "requires_gps": true,
  "gps_scan_url": "/scan/HUB-A?parcel_id=MED-104",
  "message": "RFID and temperature captured. Awaiting phone GPS proof."
}
```

The frontend `/scan/:hubId` page then submits browser GPS to `POST /scan`, keeping the backend as the source of truth for trust and routing decisions.

## Completed hardware scan response

When GPS is present and ImmuneNet completes validation, the response includes both frontend/backend fields and firmware-friendly actuator fields:

```json
{
  "status": "hardware_scan_completed",
  "accepted": true,
  "decision": "ACCEPTED",
  "action": "UPDATE_LOCATION",
  "led": "GREEN",
  "message": "Movement accepted because identity, GPS geofence, route validity, speed plausibility, temperature, and tamper checks passed."
}
```

The same scan also writes ledger events and broadcasts WebSocket updates consumed by the frontend dashboard.
