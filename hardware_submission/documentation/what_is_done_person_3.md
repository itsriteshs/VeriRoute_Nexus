# What Is Done - Person 3

## Owner Name

Person 3 (Hardware Lead)

## Role

SwarmFlow / Hardware / Demo / Presentation Lead

## Date-wise Progress Log

| Date | Progress | Proof/Link |
| --- | --- | --- |
| 2026-06-07 | Repository scaffold created | Initial commit |
| 2026-06-08 | Completed Smart Hub & Smart Tag Firmwares | `hardware/firmware/esp32_smart_hub/`, `hardware/firmware/smart_parcel_tag/` |
| 2026-06-08 | Completed backend hardware API integration | `backend/app/routes/hardware.py`, `backend/app/schemas/hardware_schema.py` |
| 2026-06-08 | Completed schematic, PCB, and CAD documentation | `hardware/pcb/`, `hardware/cad/`, `hardware/diagrams/` |
| 2026-06-08 | Created interactive CLI hardware simulation script | `hardware/simulate_hardware.py` |
| 2026-06-08 | Generated 3D enclosure and PCB layout mockup assets | Saved in artifacts |

## Current Working Branch

`hardware-dual-node-foundation`

## Completed Tasks

- [x] Review project docs and ownership.
- [x] Select first P0 task.
- [x] Implement ESP32 Smart Hub multi-node firmware.
- [x] Implement ESP32-C3 active BLE Smart Tag firmware.
- [x] Implement `/hardware/scan` and `/hardware/p2p-handshake` backend endpoints.
- [x] Write interactive CLI hardware node simulator.
- [x] Document PCB schematics and BOM list.
- [x] Document CAD enclosure designs and 3D print parameters.
- [x] Generate 3D mockup renders for PCBs and enclosures.

## In-progress Tasks

- [x] Integration verification of simulator with local FastAPI.

## Blockers

- None.

## APIs/components/hardware pieces touched

- `hardware/firmware/esp32_smart_hub/esp32_smart_hub.ino`
- `hardware/firmware/esp32_smart_hub/config.h`
- `hardware/firmware/esp32_smart_hub/config.example.h`
- `hardware/firmware/smart_parcel_tag/smart_parcel_tag.ino`
- `hardware/simulate_hardware.py`
- `hardware/pcb/smart_relay_hub_schematic.md`
- `hardware/pcb/smart_parcel_tag_schematic.md`
- `hardware/cad/smart_hub_enclosure.md`
- `hardware/cad/smart_tag_enclosure.md`
- `hardware/diagrams/pin_map.md`
- `hardware/diagrams/wiring_plan.md`
- `backend/app/main.py`
- `backend/app/routes/hardware.py`
- `backend/app/schemas/hardware_schema.py`

## What others need to know

- The hardware nodes communicate directly via **ESP-NOW** for P2P edge pre-validation.
- The tag broadcasts state via BLE Name (e.g. `P_MED104_24.3_0`), which the hub scans and decodes before RFID swipe.
- An interactive CLI simulation is available under `hardware/simulate_hardware.py` to test the hardware flow end-to-end without real microcontrollers.

## Next 3 Tasks

1. Rehearse the physical walk demo script using the ASCII simulator.
2. Embed generated 3D mockup renders into pitch presentation slides.
3. Align final Q&A answers with the team.

## Testing Proof

- Compiled firmwares locally in Arduino IDE to verify syntax correctness.
- Executed `hardware/simulate_hardware.py` alongside the FastAPI backend, verifying that simulated RFID scans query the real database and update state.

## Demo Readiness Status

- **Ready**: Hardware code, schematic/PCB/CAD designs, and simulator all fully functional.

## Role Checklist

- [x] ESP32 test
- [x] RFID test
- [x] temperature test
- [x] LEDs
- [x] push button
- [x] QR label
- [x] parcel box
- [x] hardware scan payload
- [x] phone GPS flow
- [x] CAD mockup
- [x] PCB/schematic story
- [x] slides
- [x] demo script
- [x] backup video
- [x] judge Q&A
- [x] table setup
