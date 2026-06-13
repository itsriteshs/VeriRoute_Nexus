# Smart Relay Hub Schematic & PCB Specification

This document details the PCB schematic design, trace routing strategies, and Bill of Materials (BOM) for the **Smart Relay Hub**.

---

## 1. Schematic & PCB Connections

The Smart Relay Hub is built around the `ESP32-C3-DevKitM-1` module footprint. The custom v2 PCB is located at [SmartRelayHub_v2.kicad_pcb](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartRelayHub_v2.kicad_pcb). It acts as a custom routing shield board that connects the ESP32-C3 module to the OLED and RFID headers. Other components (DHT22, LEDs, buzzer, button) are off-board and wired directly to the designated breakout pads.

### 1.1 Netlist Connections (v2 PCB Routing)
* **Power & GND**:
  + `+3.3V`: Regulated output from the ESP32-C3 module (Pad 15), routed to OLED header VCC (Pin 2) and RFID header VCC (Pin 1).
  + `GND`: Common ground pour, connecting ESP32-C3 ground (Pads 1, 16), OLED GND (Pin 1), and RFID GND (Pin 3).
* **I2C Bus (SSD1306 OLED Header)**:
  + Net `I2C_SCL` -> ESP32-C3 Pad 2 -> OLED SCL (Pin 3)
  + Net `I2C_SDA` -> ESP32-C3 Pad 3 -> OLED SDA (Pin 4)
* **SPI Bus (RC522 RFID Header)**:
  + Net `RFID_RST` -> ESP32-C3 Pad 5 -> RFID RST (Pin 2)
  + Net `SPI_MOSI` -> ESP32-C3 Pad 6 -> RFID MOSI (Pin 6)
  + Net `SPI_MISO` -> ESP32-C3 Pad 7 -> RFID MISO (Pin 5)
  + Net `SPI_SCK` -> ESP32-C3 Pad 8 / 10 -> RFID SCK (Pin 7)
  + Net `RFID_CS` -> ESP32-C3 Pad 9 / 11 -> RFID SDA/CS (Pin 8)
* **Breakout/Unrouted Nets (Off-Board Connections)**:
  + Net `BUZZER` -> ESP32-C3 Pad 4 (connects to external active buzzer)
  + Net `DHT_DATA` -> ESP32-C3 Pad 14 / 19 (connects to external DHT22 sensor data line)
  + Net `LED_GREEN` -> ESP32-C3 Pad 22 (connects to external green status LED)
  + Net `LED_RED` -> ESP32-C3 Pad 23 (connects to external red status LED)

---

## 2. Bill of Materials (BOM)

| Designator | Qty | Value / Component | Package | Description | Reference Cost (INR) |
| --- | --- | --- | --- | --- | --- |
| **U1** | 1 | ESP32-C3-DevKitM-1 | 30-Pin Module | Main micro-controller board | 200.00 |
| **U2** | 1 | RC522 RFID Reader | Header 1x8 | 13.56MHz RFID Reader board | 180.00 |
| **DISP1** | 1 | SSD1306 OLED (0.96") | Header 1x4 (I2C) | 128x64 pixels monochrome screen | 200.00 |
| **SEN1** | 1 | DHT22 Sensor (ASAIR AM2302) | SIP-4 | Temperature & Humidity Sensor | 220.00 |
| **D1** | 1 | Green LED | T-1 3/4 (5mm) | Status LED: Accepted Scan (wired) | 5.00 |
| **D2** | 1 | Red LED | T-1 3/4 (5mm) | Status LED: Anomaly/Error (wired) | 5.00 |
| **R1, R2** | 2 | 220 Ohm | Axial-0.25W | Current limiting resistors for LEDs | 2.00 |
| **R3, R4** | 2 | 4.7k Ohm | Axial-0.25W | I2C SDA/SCL pull-up resistors | 2.00 |
| **R5** | 1 | 10k Ohm | Axial-0.25W | DHT22 pull-up resistor | 1.00 |
| **BZ1** | 1 | Active 5V Buzzer | TH circular | 5V Active Piezo Audio Indicator | 20.00 |
| **SW1** | 1 | Tactile Button | 6x6mm TH | Interrupt Trigger/Simulated Event | 10.00 |

---

## 3. PCB Layout & Design Details
* **Board Format**: Custom breakout shield. The layout is available in the KiCad v8 project files:
  - KiCad PCB: [SmartRelayHub_v2.kicad_pcb](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartRelayHub_v2.kicad_pcb)
  - KiCad Project: [SmartRelayHub_v2.kicad_pro](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/pcb/SmartRelayHub_v2.kicad_pro)
* **Ground Planes**: Continuous ground pour on both top and bottom copper layers (2-layer board design) to shield signals and stabilize wireless transmission.
