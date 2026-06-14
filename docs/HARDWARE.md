# Hardware

PacketFlow ImmuneNet includes a hardware-ready SmartHub and Smart Parcel Tag package. In the MVP, judges can evaluate firmware, wiring, CAD/PCB documentation, backend payload support, and a Python simulator. Physical device operation should be shown with a video or live setup if available.

## SmartHub Concept

A SmartHub Relay Node verifies a parcel handoff at the edge:

- RFID or QR identifies the parcel.
- GPS/geofence proves the scanner/hub location at scan time.
- Temperature validates cold-chain state.
- Tamper input indicates physical breach.
- LED/OLED/buzzer gives immediate edge feedback.
- ESP-NOW relay messages share trust context between nearby hubs.
- BLE can read Smart Parcel Tag broadcasts.

## Files

| Artifact | Path |
| --- | --- |
| SmartHub firmware | `hardware_submission/firmware/esp32_smart_hub/esp32_smart_hub.ino` |
| SmartHub config template | `hardware_submission/firmware/esp32_smart_hub/config.example.h` |
| Smart Parcel Tag firmware | `hardware_submission/firmware/smart_parcel_tag/smart_parcel_tag.ino` |
| Hardware simulator | `hardware_submission/simulation/simulate_hardware.py` |
| Pin map | `hardware_submission/diagrams/pin_map.md` |
| Wiring plan | `hardware_submission/diagrams/wiring_plan.md` |
| CAD docs | `hardware_submission/cad/`, `hardware_submission/documentation/` |
| PCB docs | `hardware_submission/pcb/` |

## ESP32 / RFID / QR / GPS / Temperature / LED

SmartHub payloads can include:

```json
{
  "device_id": "ESP32-HUB-A-01",
  "hub_id": "HUB-A",
  "parcel_id": "MED-104",
  "rfid_uid": "04A8B9C104",
  "qr_payload": "http://localhost:5173/scan/HUB-A?parcel_id=MED-104",
  "temperature_c": 24.3,
  "button_pressed": false,
  "lat": 11.0168,
  "lng": 76.9558,
  "ble_verified": true,
  "ble_rssi_m": 0.63,
  "esp_now_prior_acceptance": false
}
```

Backend endpoint:

```text
POST /hardware/scan
```

If GPS is missing, the backend can return `requires_gps: true` and a scan URL for phone-based GPS completion.

## Dual-Node SwarmFlow Relay Network

The hardware submission models two physical hubs:

- `HUB-A`: central smart hub.
- `HUB-B`: relay smart hub.

The backend supports:

```text
POST /hardware/p2p-handshake
```

Example:

```json
{
  "sender_hub": "HUB-A",
  "receiver_hub": "HUB-B",
  "parcel_id": "MED-104",
  "message_type": "TRUST_SYNC",
  "trust_delta": 0.02,
  "eta_sec": 300
}
```

## ESP-NOW Inter-Hub Handshake

ESP-NOW is hardware-ready/planned in firmware and simulated/backend-supported for MVP evaluation. The endpoint records `p2p_handshake` events and can trigger trust/metric updates.

## Smart Parcel Tag BLE Beacon

The simulator uses BLE-style tag data such as parcel ID, temperature, tamper state, and RSSI estimate. Firmware exists for the smart tag. Production BLE identity security is roadmap work.

## Hardware Fallback Plan

| Failure | Fallback |
| --- | --- |
| RFID reader unavailable | Use QR/manual scan. |
| GPS unavailable | Use phone scan URL with demo coordinates. |
| Temperature sensor unavailable | Use `/scenario/temp-breach`. |
| ESP-NOW unavailable | Use `/hardware/p2p-handshake` curl or simulator. |
| Physical device unavailable | Use `python3 hardware_submission/simulation/simulate_hardware.py`. |

## What Judges Should Understand

The MVP does not depend on judges trusting a mocked hardware claim. The backend accepts hardware-native payloads, validates them through the same ImmuneNet path as manual scans, and logs evidence into the same ledger. The hardware package demonstrates readiness for physical proof, while the software demo remains runnable without devices.
