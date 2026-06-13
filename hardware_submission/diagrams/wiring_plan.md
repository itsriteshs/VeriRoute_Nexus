# Hardware Wiring Plan & Integration Guide

This document describes the wiring instructions and circuit guidelines for assembling the PacketFlow hardware modules, supporting both development breadboard wiring and custom v2 PCB shield assembly.

---

## 1. Smart Relay Hub

The Smart Relay Hub can be assembled either on a breadboard for rapid testing or using the custom v2 PCB shield board (`SmartRelayHub_v2.kicad_pcb`).

### 1.1 Development Breadboard Wiring (Firmware-Compatible)

For standard development and testing, map the connections directly to the development board pins:

1. **Power Off**: Ensure the micro-controller is disconnected from USB power before making any connections.
2. **Breadboard Mount**: Place the ESP32 dev board on a breadboard bridging the middle divider.
3. **RFID Reader (RC522)**:
   - Connect **RFID 3.3V** to **ESP32 3.3V** (do NOT use 5V/VIN, otherwise the RC522 chip will burn).
   - Connect **RFID GND** to **ESP32 GND**.
   - Connect SPI lines: **SDA** to **GPIO 5**, **SCK** to **GPIO 18**, **MISO** to **GPIO 19**, **MOSI** to **GPIO 23**, and **RST** to **GPIO 22**.
4. **OLED Screen (SSD1306)**:
   - Connect **OLED VCC** to **ESP32 3.3V** and **GND** to **ESP32 GND**.
   - Connect I2C lines: **SDA** to **GPIO 21** and **SCL** to **GPIO 22**.
5. **DHT22 Temperature Sensor**:
   - Connect **VCC** to **3.3V** and **GND** to **GND**.
   - Connect **DATA** to **GPIO 32** with a **10k Ohm resistor** between the Data and VCC lines as a pull-up.
6. **LED Indicators & Buzzer**:
   - Connect **GPIO 25** to a **220-ohm resistor**, then to the anode (long leg) of the **Green LED**. Connect the cathode (short leg) to **GND**.
   - Connect **GPIO 26** to a **220-ohm resistor**, then to the anode of the **Red LED**. Connect the cathode to **GND**.
   - Connect the active buzzer's positive pin to **GPIO 14** and the negative pin to **GND**.
7. **Tactile Push Button**:
   - Connect one terminal of the button to **GPIO 27** and the other terminal to **GND** (relies on internal pull-up).

### 1.2 Custom v2 PCB Shield Assembly

If assembling the custom v2 PCB board:
1. Solder female header sockets onto the PCB for the **ESP32-C3-DevKitM-1** module (`U1`), the **SSD1306 OLED** display (`DISP1`), and the **RC522 RFID Reader** (`U2`).
2. Solder the active buzzer, DHT22 sensor, LEDs, and tactile button off-board, wiring them directly to the corresponding breakout pads on the board:
   - **Buzzer**: Connect to ESP32-C3 module Pad 4 (`BUZZER`) and GND.
   - **DHT22**: Connect data to Pad 14 / 19 (`DHT_DATA`), VCC to Pad 15 (`+3.3V`), and GND to GND.
   - **Green LED**: Connect anode to Pad 22 (`LED_GREEN`) and cathode to GND.
   - **Red LED**: Connect anode to Pad 23 (`LED_RED`) and cathode to GND.

---

## 2. Smart Parcel Tag

The active Smart Parcel Tag utilizes the **ESP32-C3-DevKitM-1** module and the custom sensor shield (`SmartParcelTag_v2.kicad_pcb`).

### 2.1 Breadboard Connections
* **DHT22 Sensor**: Connect VCC to 3.3V, GND to GND, and Data to GPIO 4.
* **Tamper Switch**: Connect a micro limit switch between GPIO 2 and GND. (Normally-closed; reads HIGH when the box lid is removed).

### 2.2 Custom v2 PCB Shield Assembly
1. Solder the ESP32-C3 module (`U1`), DHT22 sensor (`SEN1`), JST battery input connector (`CONN1`), SMD resistor `R1` (10k Ohm), and SMD capacitor `C1` (10uF) directly to the PCB.
2. Wire the off-board micro limit switch (tamper switch) directly between Pad 4 (GPIO 2) and GND.
3. Plug a 3.7V rechargeable LiPo battery into the JST connector (`CONN1`).

---

## 3. Power Safety Warnings
> [!CAUTION]
> * Never share the 5V/VIN line directly with the RC522 RFID reader; it operates strictly at 3.3V levels.
> * Always double check the pin maps for your specific dev board manufacturer, as pin positions vary between ESP32 dev board revisions.
