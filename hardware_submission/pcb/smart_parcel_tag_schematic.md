# Smart Parcel Tag Schematic & PCB Specification

This document details the PCB schematic design, power management, and Bill of Materials (BOM) for the active **Smart Parcel Tag**.

---

## 1. Schematic & PCB Connections

The Smart Parcel Tag is an ultra-compact, low-power active BLE beacon built around the `ESP32-C3-DevKitM-1` module footprint. The custom v2 PCB is located at [SmartParcelTag_v2.kicad_pcb](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartParcelTag_v2.kicad_pcb). It hosts the temperature sensor and power filtering, while the tamper limit switch is wired directly to the development board headers.

### 1.1 Netlist Connections (v2 PCB Routing)
* **Power & GND**:
  + `+3.3V` Rail: Connects JST battery connector positive input (Pin 1), decoupling capacitor C1, pull-up resistor R1, DHT22 sensor power input (Pin 1), and ESP32-C3 module power inputs (Pads 8, 15).
  + `GND` Rail: Common ground pour connecting JST battery connector negative input (Pin 2), decoupling capacitor C1, DHT22 sensor ground (Pin 3), and ESP32-C3 module ground (Pad 1).
* **DHT22 Net**:
  + Net `DHT_DATA` connects DHT22 sensor data (Pin 2) directly to ESP32-C3 Pad 7. It is pulled up to `+3.3V` via a 10k Ohm SMD resistor (R1).
* **Off-Board/External Nets**:
  + **Tamper Switch**: Wire a micro limit switch directly between ESP32-C3 Pad 4 (GPIO 2) and GND (off-board; not routed on the custom sensor shield PCB).
  + **Status LED**: ESP32-C3 GPIO 8 controls the onboard blue status LED.

---

## 2. Bill of Materials (BOM)

| Designator | Qty | Value / Component | Package | Description | Reference Cost (INR) |
| --- | --- | --- | --- | --- | --- |
| **U1** | 1 | ESP32-C3-DevKitM-1 | 30-Pin Module | Main micro-controller board | 200.00 |
| **SEN1** | 1 | DHT22 Sensor (ASAIR AM2302) | SIP-4 | Temperature & Humidity Sensor | 220.00 |
| **SW1** | 1 | Micro Limit Switch | Wired Switch | Tamper lever switch (normally closed; off-board) | 15.00 |
| **R1** | 1 | 10k Ohm | SMD 0805 | Pull-up resistor for DHT22 data line | 1.00 |
| **C1** | 1 | 10uF | SMD 0805 | Bypass filter capacitor across 3.3V | 2.00 |
| **BT1** | 1 | 3.7V 500mAh LiPo | LiPo pouch | Rechargeable battery cell | 150.00 |
| **CONN1**| 1 | JST PH 2.0 2-Pin | Right-Angle SMD | Battery quick-connect header | 10.00 |

---

## 3. PCB Layout & Design Details
* **Board Format**: Custom sensor shield board. The design is available in the KiCad v8 project files:
  - KiCad PCB: [SmartParcelTag_v2.kicad_pcb](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartParcelTag_v2.kicad_pcb)
  - KiCad Project: [SmartParcelTag_v2.kicad_pro](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartParcelTag_v2.kicad_pro)
* **Antenna Keepout**: No copper traces or ground planes are placed under the ESP32-C3's PCB trace antenna region (defined on the breakout) to prevent wireless signal degradation.
