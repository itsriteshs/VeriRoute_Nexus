# Hardware Wiring Plan & Integration Guide

This document describes the complete wiring instructions and circuit guidelines for assembling the PacketFlow hardware modules.

---

## 1. Smart Relay Hub (ESP32 DevKit v1)

### 1.1 Assembly Diagram Representation
```
       +--------------------------------------------+
       |               ESP32 DevKit                 |
       |  3.3V  GND  G5   G18  G19  G23  G22  G21 G22 |
       +----+----+----+----+----+----+----+----+----+
            |    |    |    |    |    |    |    |   |
            |    |    +----+----+----+----+    |   |  (SPI interface)
            |    |         |    |    |    |    |   |
       +----+----+----+----+----+----+----+    |   |
       | 3.3V   GND  SDA  SCK  MISO MOSI RST  |   |
       |            RC522 RFID Reader         |    |   |
       +--------------------------------------+    |   |
                                                   |   |  (I2C interface)
                                              +----+---+----+
                                              | SDA  SCL GND VCC
                                              | SSD1306 OLED|
                                              +-------------+
```

### 1.2 Step-by-Step Wiring Sequence
1. **Power Off**: Ensure the ESP32 is disconnected from USB power before making any connections.
2. **Breadboard Mount**: Place the ESP32 on a breadboard bridging the middle divider.
3. **RFID Reader**:
   - Connect **RFID 3.3V** to **ESP32 3.3V** (do NOT use 5V/VIN, otherwise the RC522 chip will burn).
   - Connect **RFID GND** to **ESP32 GND**.
   - Connect **SDA** to **GPIO 5**, **SCK** to **GPIO 18**, **MISO** to **GPIO 19**, **MOSI** to **GPIO 23**, and **RST** to **GPIO 22**.
4. **OLED Screen**:
   - Connect **OLED VCC** to **ESP32 3.3V** and **GND** to **ESP32 GND**.
   - Connect **OLED SDA** to **ESP32 GPIO 21** and **OLED SCL** to **ESP32 GPIO 22**.
5. **DHT22 Temperature Sensor**:
   - Connect **VCC** to **3.3V** and **GND** to **GND**.
   - Connect **DATA** to **GPIO 32**.
   - Place a **10k Ohm resistor** between the Data pin and VCC pin as a pull-up.
6. **LED Indicators**:
   - Connect **GPIO 25** to a **220-ohm resistor**, then to the anode (long leg) of the **Green LED**. Connect the cathode (short leg) to **GND**.
   - Connect **GPIO 26** to a **220-ohm resistor**, then to the anode (long leg) of the **Red LED**. Connect the cathode to **GND**.
7. **Buzzer**:
   - Connect the positive pin of the buzzer to **GPIO 14** and the negative pin to **GND**.
8. **Push Button**:
   - Connect one terminal of the button to **GPIO 27** and the other terminal to **GND**. (Internal pull-up is enabled in firmware).

---

## 2. Smart Parcel Tag (ESP32-C3 Super Mini)

### 2.1 Circuit Structure
* The Smart Parcel Tag is designed for low power. It utilizes an `ESP32-C3` chip powered by a 3.7V LiPo battery.
* **DHT22 Sensor**: Connect VCC to 3.3V, GND to GND, and Data to GPIO 4.
* **Tamper Switch**: Connect a micro limit switch between GPIO 2 and GND. The firmware uses internal pull-up. The switch is mounted in the box such that the switch is CLOSED (LOW) when the box lid is shut, and OPENS (reading HIGH via pull-up) when the lid is removed.

---

## 3. Power Safety Warnings
> [!CAUTION]
> * Never share the 5V/VIN line directly with the RC522 RFID reader; it operates strictly at 3.3V levels.
> * Always double check the pin maps for your specific dev board manufacturer, as pin positions vary between ESP32 dev board revisions.
