# Hardware Pin Map Specification

This document defines the physical pin connections and nets for both the **Smart Relay Hub** and the **Smart Parcel Tag**, covering both the breadboard firmware GPIO mapping and the custom v2 PCB shield routing.

---

## 1. Smart Relay Hub

The Smart Relay Hub controller firmware runs on an ESP32. In the v2 hardware layout, the custom breakout board uses the **ESP32-C3-DevKitM-1** module footprint.

### 1.1 Pin Mapping Table

| Component | Function | Firmware/Breadboard GPIO | v2 PCB Shield Pad | Notes / Net Names |
| :--- | :--- | :--- | :--- | :--- |
| **MFRC522 RFID** | VCC | **3.3V** | **Pad 15** (`+3.3V`) | Must be 3.3V power (not 5V) |
| | GND | **GND** | **Pad 1/16** (`GND`) | Ground connection |
| | SDA (CS) | **GPIO 5** | **Pad 9 / 11** (`RFID_CS`) | SPI Chip Select |
| | SCK | **GPIO 18** | **Pad 8 / 10** (`SPI_SCK`) | SPI Clock |
| | MISO | **GPIO 19** | **Pad 7** (`SPI_MISO`) | SPI Master-In Slave-Out |
| | MOSI | **GPIO 23** | **Pad 6** (`SPI_MOSI`) | SPI Master-Out Slave-In |
| | RST | **GPIO 22** | **Pad 5** (`RFID_RST`) | Reset |
| **SSD1306 OLED** | VCC | **3.3V** | **Pad 15** (`+3.3V`) | 3.3V power |
| | GND | **GND** | **Pad 1/16** (`GND`) | Ground |
| | SCL | **GPIO 22** | **Pad 2** (`I2C_SCL`) | I2C Clock |
| | SDA | **GPIO 21** | **Pad 3** (`I2C_SDA`) | I2C Data |
| **DHT22 Sensor** | VCC | **3.3V** | **Pad 15** (`+3.3V`) | 3.3V power |
| | GND | **GND** | **Pad 1/16** (`GND`) | Ground |
| | Data | **GPIO 32** | **Pad 14 / 19** (`DHT_DATA`) | Add 10k pull-up resistor to VCC |
| **Indicators** | Green LED | **GPIO 25** | **Pad 22** (`LED_GREEN`) | Connect with 220-ohm current-limiting resistor |
| | Red LED | **GPIO 26** | **Pad 23** (`LED_RED`) | Connect with 220-ohm current-limiting resistor |
| | Buzzer | **GPIO 14** | **Pad 4** (`BUZZER`) | Active 5V Piezo Buzzer (high trigger) |
| **Controls** | Push Button | **GPIO 27** | *Not Routed* | Toggles ground (internally pulled HIGH; off-board) |

---

## 2. Smart Parcel Tag

The active Smart Parcel Tag utilizes a compact **ESP32-C3-DevKitM-1** module to read condition sensors and advertise its payload over BLE.

### 2.1 Pin Mapping Table

| Component | Function | Firmware/Breadboard GPIO | v2 PCB Shield Pad | Notes / Net Names |
| :--- | :--- | :--- | :--- | :--- |
| **DHT22 Sensor** | VCC | **3.3V** | **Pad 8 / 15** (`+3.3V`) | 3.3V power |
| | GND | **GND** | **Pad 1** (`GND`) | Ground |
| | Data | **GPIO 4** | **Pad 7** (`DHT_DATA`) | Sensor temperature broadcast |
| **Controls** | Tamper Switch | **GPIO 2** | *Not Routed* | Wired directly between Pad 4 and GND (off-board) |
| **Indicators** | Status LED | **GPIO 8** | *Onboard* | Built-in blue status LED on ESP32-C3 DevKit |
| **Power** | Battery Input | **RAW/5V** | **Pad 8 / 15** (`+3.3V`) | Powered via JST 2.0 connector to 3.3V rail |
| | Battery GND | **GND** | **Pad 1** (`GND`) | Common ground |

