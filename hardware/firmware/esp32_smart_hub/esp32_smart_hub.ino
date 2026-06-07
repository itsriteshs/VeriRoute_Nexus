// Owner: Person 3 — Hardware + Demo + Presentation Lead
// Purpose: ESP32 Smart Relay Hub firmware placeholder.

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";
const char* BACKEND_URL = "http://localhost:8000/hardware/scan";

const int GREEN_LED_PIN = 25;
const int RED_LED_PIN = 26;
const int BUTTON_PIN = 27;
const int TEMP_SENSOR_PIN = 32;

void setup() {
  Serial.begin(115200);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  // TODO: WiFi config, RFID placeholder, temperature placeholder, LED behavior, push button flow.
}

void loop() {
  // TODO: POST /hardware/scan with this JSON:
  // {"device_id":"ESP32-HUB-A-01","hub_id":"HUB-A","parcel_id":"MED-104","rfid_uid":"RFID-DEMO-104","qr_payload":"http://localhost:5173/scan/HUB-A?parcel_id=MED-104","temperature_c":24.3,"button_pressed":true,"lat":12.9716,"lng":77.5946,"timestamp":"2026-06-07T10:00:00Z"}
}
