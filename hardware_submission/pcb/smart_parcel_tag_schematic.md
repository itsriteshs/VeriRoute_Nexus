# Smart Parcel Tag Schematic & PCB Specification

This document details the PCB schematic design, power management, and Bill of Materials (BOM) for the active **Smart Parcel Tag**.

---

## 1. Schematic Design Details

The Smart Parcel Tag is a ultra-compact, low-power active BLE beacon built around the `ESP32-C3 Super Mini`. It monitors temperature via a DHT22 sensor and tracks package box security using a tamper limit switch.

### 1.1 Schematic Netlist Connections
* **Power Nets**:
  + `VBAT`: Routed from the positive terminal of a 3.7V LiPo battery directly to the battery charger inputs and the ESP32-C3's regulator input (`VBUS` or `RAW` pin).
  + `+3.3V`: Regulated 3.3V power rails, decoupling sensor noise via capacitors.
  + `GND`: Common ground pour connecting all components.
* **Tamper Switch Net**:
  + Net `TAMPER_SW` -> ESP32-C3 GPIO 2. The switch connects GPIO 2 directly to GND when closed.
* **DHT22 Net**:
  + Net `DHT_DATA` -> ESP32-C3 GPIO 4 (pulled-up to 3.3V with a 10k resistor).
* **Onboard Indicators**:
  + Net `STATUS_LED` -> ESP32-C3 GPIO 8 -> internal current limiting resistor -> Blue status LED.

---

## 2. Bill of Materials (BOM)

| Designator | Qty | Value / Component | Package | Description | Reference Cost (INR) |
| --- | --- | --- | --- | --- | --- |
| **U1** | 1 | ESP32-C3 Super Mini | SMD modules | RISC-V Bluetooth/WiFi MCU board | 200.00 |
| **SEN1** | 1 | DHT22 Sensor | SIP-4 | Temperature & Humidity Sensor | 220.00 |
| **SW1** | 1 | Micro Limit Switch | SMD Tactile | Tamper lever switch (normally closed) | 15.00 |
| **R1** | 1 | 10k Ohm | SMD 0805 | Pull-up resistor for DHT22 data line | 1.00 |
| **C1** | 1 | 10uF | SMD 0805 | Filter capacitor across 3.3V | 2.00 |
| **BT1** | 1 | 3.7V 500mAh LiPo | LiPo pouch | Rechargeable battery cell | 150.00 |
| **CONN1**| 1 | JST 2.0 2-Pin | Right-Angle SMD | Battery quick connect port | 10.00 |

---

## 3. PCB Layout Guidelines
* **Miniaturization**: Route with compact **0.203mm** (8 mils) trace widths to keep the layout within a circular board footprint of under **35mm diameter**.
* **Antenna Keepout**: Do not route any copper traces, ground pours, or power planes underneath the ESP32-C3's PCB antenna area. Keep this region completely clear of metal on both layers to avoid reducing BLE broadcast range.

---

## 4. Visual Layout Render

Below is the PCB layout mockup generated for the Smart Parcel Tag:

![Smart Parcel Tag PCB Layout Render](file:///C:/Users/mouli/.gemini/antigravity-ide/brain/d29bc1cd-6a5f-4263-8353-0f507c8aa48f/smart_tag_pcb_1780932141188.png)
