# Hardware Pin Map Specification

This document defines the exact pin connections for both the **Smart Relay Hub (ESP32 DevKit v1)** and the **Smart Parcel Tag (ESP32-C3 Super Mini)**.

---

## 1. Smart Relay Hub (ESP32 DevKit v1)

The Smart Relay Hub controller is an ESP32 (30-pin or 38-pin DevKit). It connects to an RC522 RFID reader, an SSD1306 OLED screen, a DHT22 temperature/humidity sensor, status indicators, and controls.

| Component | Pin Function | ESP32 GPIO | Color / Connection Code | Notes |
| --- | --- | --- | --- | --- |
| **MFRC522 RFID** | SDA (SS) | **GPIO 5** | Yellow | SPI Chip Select |
| | SCK | **GPIO 18** | Green | SPI Clock |
| | MOSI | **GPIO 23** | Blue | SPI Master-Out Slave-In |
| | MISO | **GPIO 19** | Violet | SPI Master-In Slave-Out |
| | RST | **GPIO 22** | Orange | Reset Pin |
| | GND | **GND** | Black | Ground |
| | 3.3V | **3.3V** | Red | **Must be 3.3V power (not 5V)** |
| **SSD1306 OLED** | SDA | **GPIO 21** | Blue | I2C Data (default) |
| | SCL | **GPIO 22** | Yellow | I2C Clock (default) |
| | GND | **GND** | Black | Ground |
| | VCC | **3.3V** | Red | 3.3V power |
| **DHT22 Sensor** | Data | **GPIO 32** | White | Add 10k pull-up resistor to VCC |
| | VCC | **3.3V** | Red | 3.3V power |
| | GND | **GND** | Black | Ground |
| **Indicators** | Green LED | **GPIO 25** | Green | Connect with 220-ohm current-limiting resistor |
| | Red LED | **GPIO 26** | Red | Connect with 220-ohm current-limiting resistor |
| | Buzzer | **GPIO 14** | Grey | Active 5V Piezo Buzzer (high trigger) |
| **Controls** | Push Button | **GPIO 27** | Brown | Toggles ground (internally pulled HIGH) |

---

## 2. Smart Parcel Tag (ESP32-C3 Super Mini)

The active Smart Parcel Tag utilizes a highly compact ESP32-C3 board to read condition sensors and advertise its payload over BLE.

| Component | Pin Function | ESP32-C3 GPIO | Connection Code | Notes |
| --- | --- | --- | --- | --- |
| **DHT22 Sensor** | Data | **GPIO 4** | White | Sensor temperature broadcast |
| | VCC | **3.3V** | Red | 3.3V Power |
| | GND | **GND** | Black | Ground |
| **Controls** | Tamper Switch | **GPIO 2** | Blue | Micro limit switch (normally-closed to GND) |
| **Indicators** | Status LED | **GPIO 8** | Onboard | Onboard blue status LED |
| **Power** | Battery Input | **RAW/5V** | JST 2.0 Connector | 3.7V LiPo Battery input |
| | Battery GND | **GND** | Black | Common Ground |
