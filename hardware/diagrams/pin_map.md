# ESP32 Pin Map

| Component | Suggested Pin | Notes |
| --- | --- | --- |
| RC522 RFID SDA/SS | GPIO 5 | Verify with SPI library examples |
| RC522 RFID SCK | GPIO 18 | SPI clock |
| RC522 RFID MOSI | GPIO 23 | SPI MOSI |
| RC522 RFID MISO | GPIO 19 | SPI MISO |
| RC522 RFID RST | GPIO 22 | Reset pin |
| DHT22/SHT31 data | GPIO 32 | Verify voltage and pull-up |
| Green LED | GPIO 25 | Accepted scan |
| Red LED | GPIO 26 | Blocked scan or backend error |
| Push button | GPIO 27 | Use input pull-up |

Verify actual wiring against the board pinout before connecting power.
