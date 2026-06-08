# Smart Relay Hub Schematic & PCB Specification

This document details the PCB schematic design, trace routing strategies, and Bill of Materials (BOM) for the **Smart Relay Hub**.

---

## 1. Schematic Design Details

The schematic is designed using standard 0.1-inch header connectors for pluggable development modules, minimizing component cost and streamlining hand-assembly.

### 1.1 Schematic Netlist Connections
* **Power Nets**:
  + `+5V`: Derived from USB micro-B port on the ESP32 DevKit, routed to active 5V Buzzer power pin.
  + `+3.3V`: Regulated output from the ESP32's onboard LDO. Routed to RFID VCC, OLED VCC, and DHT22 VCC.
  + `GND`: Common ground plane connecting all modules, capacitors, and LEDs.
* **SPI Bus (RFID RC522)**:
  + Net `RFID_CS` -> ESP32 GPIO 5 (with 10k pull-up resistor to 3.3V)
  + Net `SPI_SCK` -> ESP32 GPIO 18
  + Net `SPI_MISO` -> ESP32 GPIO 19
  + Net `SPI_MOSI` -> ESP32 GPIO 23
  + Net `RFID_RST` -> ESP32 GPIO 22
* **I2C Bus (OLED SSD1306)**:
  + Net `I2C_SDA` -> ESP32 GPIO 21 (with 4.7k pull-up resistor to 3.3V)
  + Net `I2C_SCL` -> ESP32 GPIO 22 (with 4.7k pull-up resistor to 3.3V)
* **DHT22 Net**:
  + Net `DHT_DATA` -> ESP32 GPIO 32 (with 10k pull-up resistor to 3.3V)
* **Status Outputs**:
  + Net `LED_GREEN` -> ESP32 GPIO 25 -> 220-ohm resistor -> Green LED -> GND
  + Net `LED_RED` -> ESP32 GPIO 26 -> 220-ohm resistor -> Red LED -> GND
  + Net `BUZZER_CTRL` -> ESP32 GPIO 14 -> Active Buzzer positive terminal -> GND

---

## 2. Bill of Materials (BOM)

| Designator | Qty | Value / Component | Package | Description | Reference Cost (INR) |
| --- | --- | --- | --- | --- | --- |
| **U1** | 1 | ESP32 DevKit v1 | DIP-30 (Pluggable) | Main Microcontroller Board | 350.00 |
| **U2** | 1 | RC522 RFID Module | Header 1x8 | 13.56MHz RFID Reader board | 180.00 |
| **DISP1** | 1 | SSD1306 OLED (0.96") | Header 1x4 (I2C) | 128x64 pixels monochrome screen | 200.00 |
| **SEN1** | 1 | DHT22 Sensor | SIP-4 | Temperature & Humidity Sensor | 220.00 |
| **D1** | 1 | Green LED | T-1 3/4 (5mm) | Status LED: Accepted Scan | 5.00 |
| **D2** | 1 | Red LED | T-1 3/4 (5mm) | Status LED: Anomaly/Error | 5.00 |
| **R1, R2** | 2 | 220 Ohm | Axial-0.25W | Current limiting resistors for LEDs | 2.00 |
| **R3, R4** | 2 | 4.7k Ohm | Axial-0.25W | I2C SDA/SCL pull-up resistors | 2.00 |
| **R5** | 1 | 10k Ohm | Axial-0.25W | DHT22 pull-up resistor | 1.00 |
| **BZ1** | 1 | Active 5V Buzzer | TH circular | 5V Active Piezo Audio Indicator | 20.00 |
| **SW1** | 1 | Tactile Button | 6x6mm TH | Interrupt Trigger/Simulated Event | 10.00 |

---

## 3. PCB Layout Guidelines
* **Trace Width**: Power traces (`+5V`, `+3.3V`) should be routed with a minimum width of **0.5mm** (20 mils). Signals traces can be **0.254mm** (10 mils).
* **Decoupling**: Place a **0.1uF bypass capacitor** close to the power pins of the OLED and RFID module connectors to filter line noise.
* **Ground Planes**: Use a continuous ground pour on both the top and bottom copper layers (2-layer board design) to prevent signal loops and stabilize the ESP32's WiFi/Bluetooth antenna transmissions.

---

## 4. Visual Layout Render

Below is the PCB layout mockup generated for the Smart Relay Hub:

![Smart Relay Hub PCB Layout Render](file:///C:/Users/mouli/.gemini/antigravity-ide/brain/d29bc1cd-6a5f-4263-8353-0f507c8aa48f/smart_hub_pcb_1780932123795.png)
