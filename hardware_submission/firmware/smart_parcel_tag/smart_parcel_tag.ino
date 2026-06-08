// Owner: Person 3 — Hardware + Demo + Presentation Lead
// Purpose: ESP32-C3 Smart Parcel Tag BLE Beacon firmware. Monitors condition sensors and advertises state wirelessly.

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEAdvertising.h>
#include <DHT.h>

#define DHT_PIN         4
#define TAMPER_PIN      2
#define STATUS_LED_PIN  8  // Built-in LED on ESP32-C3 Super Mini is on GPIO 8

#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

BLEAdvertising *pAdvertising;
String parcel_id = "MED104"; // Short version of MED-104 (fits BLE name limits)
unsigned long last_update_time = 0;
const unsigned long UPDATE_INTERVAL_MS = 3000; // Update BLE payload every 3 seconds

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("[SETUP] Starting Smart Parcel Tag (ESP32-C3 BLE Beacon)");
    
    // Configure inputs/outputs
    pinMode(TAMPER_PIN, INPUT_PULLUP);
    pinMode(STATUS_LED_PIN, OUTPUT);
    digitalWrite(STATUS_LED_PIN, LOW); // LED off
    
    // Initialize DHT sensor
    dht.begin();
    Serial.println("[DHT] DHT22 Initialized");
    
    // Initialize BLE
    BLEDevice::init("");
    pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06);  
    pAdvertising->setMinPreferred(0x12);
    
    // First advertising update
    updateBLEAdvertisement();
}

void updateBLEAdvertisement() {
    // Read temperature
    float temp = dht.readTemperature();
    if (isnan(temp)) {
        temp = 24.3; // Default fallback
    }
    
    // Read tamper switch
    // Normally-closed: if the lid is opened, the button is released, reading HIGH.
    // So HIGH = Tampered, LOW = Secure.
    bool tampered = (digitalRead(TAMPER_PIN) == HIGH);
    
    // Format name: P_[ParcelID]_[TempFloat]_[TamperInt]
    // Example: P_MED104_24.3_0
    char name_buffer[30];
    snprintf(name_buffer, sizeof(name_buffer), "P_%s_%.1f_%d", parcel_id.c_str(), temp, tampered ? 1 : 0);
    String adv_name = String(name_buffer);
    
    Serial.printf("[BLE] Updating advertisement name to: %s\n", adv_name.c_str());
    
    // Stop advertising to update the name
    pAdvertising->stop();
    
    // Set new advertising name payload
    BLEAdvertisementData oAdvertisementData;
    oAdvertisementData.setName(adv_name.c_str());
    pAdvertising->setAdvertisementData(oAdvertisementData);
    
    // Restart advertising
    pAdvertising->start();
    
    // Flash status LED briefly to show activity
    digitalWrite(STATUS_LED_PIN, HIGH);
    delay(100);
    digitalWrite(STATUS_LED_PIN, LOW);
}

void loop() {
    unsigned long current_time = millis();
    if (current_time - last_update_time >= UPDATE_INTERVAL_MS) {
        updateBLEAdvertisement();
        last_update_time = current_time;
    }
    delay(100);
}
