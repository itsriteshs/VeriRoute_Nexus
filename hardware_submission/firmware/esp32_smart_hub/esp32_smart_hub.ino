// Owner: Person 3 — Hardware + Demo + Presentation Lead
// Purpose: ESP32 Smart Relay Hub firmware. Connects RFID, OLED, DHT22, LEDs, Buzzer, Button, BLE, and ESP-NOW.

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <esp_now.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "config.h"

// OLED Screen size
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Pin Mappings from pin_map.md
#define RFID_SS_PIN     5
#define RFID_RST_PIN    22
#define DHT_PIN         32
#define GREEN_LED_PIN   25
#define RED_LED_PIN     26
#define BUTTON_PIN      27
#define BUZZER_PIN      14

// RFID Instance
MFRC522 mfrc522(RFID_SS_PIN, RFID_RST_PIN);

// DHT Instance
#define DHTTYPE DHT22
DHT dht(DHT_PIN, DHTTYPE);

// Local Hub Properties
const char* HUB_ID = IS_HUB_A ? "HUB-A" : "HUB-B";
const char* DEVICE_ID = IS_HUB_A ? "ESP32-HUB-A-01" : "ESP32-HUB-B-01";

// BLE Scan settings
int BLE_SCAN_TIME_SECONDS = 2;
BLEScan* pBLEScan;

// Local Handshake Cache (for HUB-B receiving from HUB-A)
bool cached_prior_acceptance = false;
String cached_prior_hub = "";
float cached_trust_delta = 0.0;

// BLE Scan Results
bool ble_tag_detected = false;
String ble_parcel_id = "";
float ble_temperature = 0.0;
bool ble_tamper = false;
float ble_rssi = 0.0;

// ESP-NOW Structure
typedef struct struct_message {
    char parcel_id[32];
    char msg_type[32];
    float trust_delta;
} struct_message;

struct_message espNowMsg;

// ESP-NOW Received Callback
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
    memcpy(&espNowMsg, incomingData, sizeof(espNowMsg));
    Serial.printf("[ESP-NOW] Message received: Parcel %s, Type %s, Delta %.2f\n", 
                  espNowMsg.parcel_id, espNowMsg.msg_type, espNowMsg.trust_delta);
    
    if (strcmp(espNowMsg.msg_type, "HUB_ACCEPTED") == 0) {
        cached_prior_acceptance = true;
        cached_prior_hub = "HUB-A";
        cached_trust_delta = espNowMsg.trust_delta;
        
        // Update OLED screen to notify incoming parcel
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(WHITE);
        display.setCursor(0, 0);
        display.printf("--- %s ---\n", HUB_ID);
        display.println("STATUS: INCOMING");
        display.printf("Parcel: %s\n", espNowMsg.parcel_id);
        display.println("From: HUB-A");
        display.display();
        
        // Short double-beep to notify operators
        digitalWrite(BUZZER_PIN, HIGH); delay(50); digitalWrite(BUZZER_PIN, LOW); delay(50);
        digitalWrite(BUZZER_PIN, HIGH); delay(50); digitalWrite(BUZZER_PIN, LOW);
    }
}

// BLE Custom Scanner callback
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
        String name = advertisedDevice.getName().c_str();
        // Parse BLE name starting with P_ (e.g. P_MED104_24.3_0)
        if (name.startsWith("P_")) {
            Serial.printf("[BLE] Active Tag Found: %s\n", name.c_str());
            
            // Parse name: P_PARCELID_TEMP_TAMPER
            int firstUnderscore = name.indexOf('_');
            int secondUnderscore = name.indexOf('_', firstUnderscore + 1);
            int thirdUnderscore = name.indexOf('_', secondUnderscore + 1);
            
            if (firstUnderscore != -1 && secondUnderscore != -1) {
                String raw_parcel = name.substring(firstUnderscore + 1, secondUnderscore);
                // Reconstruct MED-104 format from MED104
                if (raw_parcel == "MED104") {
                    ble_parcel_id = "MED-104";
                } else {
                    ble_parcel_id = raw_parcel;
                }
                
                if (thirdUnderscore != -1) {
                    ble_temperature = name.substring(secondUnderscore + 1, thirdUnderscore).toFloat();
                    ble_tamper = (name.substring(thirdUnderscore + 1).toInt() == 1);
                } else {
                    ble_temperature = name.substring(secondUnderscore + 1).toFloat();
                    ble_tamper = false;
                }
                
                ble_tag_detected = true;
                ble_rssi = advertisedDevice.getRSSI();
                
                // Calculate distance estimate from RSSI (RSSI at 1m is approx -59dBm)
                // d = 10 ^ ((Measured Power – RSSI) / (10 * N))
                Serial.printf("Parsed: Parcel=%s, Temp=%.1fC, Tamper=%d, RSSI=%.1f\n", 
                              ble_parcel_id.c_str(), ble_temperature, ble_tamper, ble_rssi);
            }
        }
    }
};

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.printf("[SETUP] Starting Smart Hub Firmware as: %s\n", HUB_ID);
    
    // Initialize GPIO pins
    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    
    digitalWrite(GREEN_LED_PIN, LOW);
    digitalWrite(RED_LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    
    // Initialize OLED screen
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
        Serial.println("[OLED] SSD1306 allocation failed");
    } else {
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(WHITE);
        display.setCursor(0, 0);
        display.printf("--- %s ---\n", HUB_ID);
        display.println("Initializing...");
        display.display();
    }
    
    // Initialize SPI and RFID RC522
    SPI.begin();
    mfrc522.PCD_Init();
    Serial.println("[RFID] RC522 Initialized");
    
    // Initialize DHT sensor
    dht.begin();
    Serial.println("[DHT] DHT22 Initialized");
    
    // Initialize BLE
    BLEDevice::init(DEVICE_ID);
    pBLEScan = BLEDevice::getBLEScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true);
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);
    Serial.println("[BLE] Scanner Initialized");
    
    // Initialize WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.printf("[WiFi] Connecting to %s", WIFI_SSID);
    int retries = 0;
    while (WiFi.status() != WL_CONNECTED && retries < 15) {
        delay(500);
        Serial.print(".");
        retries++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("\n[WiFi] Connected. IP: %s\n", WiFi.localIP().toString().c_str());
    } else {
        Serial.println("\n[WiFi] Failed to connect. Operating in offline/ESP-NOW fallback mode.");
    }
    
    // Initialize ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("[ESP-NOW] Error initializing ESP-NOW");
    } else {
        Serial.println("[ESP-NOW] Initialized successfully");
        esp_now_register_recv_cb(OnDataRecv);
        
        // Register peer
        esp_now_peer_info_t peerInfo;
        memcpy(peerInfo.peer_addr, PEER_MAC, 6);
        peerInfo.channel = 0;  
        peerInfo.encrypt = false;
        
        if (esp_now_add_peer(&peerInfo) != ESP_OK) {
            Serial.println("[ESP-NOW] Failed to add peer");
        } else {
            Serial.println("[ESP-NOW] Peer node registered successfully");
        }
    }
    
    // Display Standby State on OLED
    updateOledStandby();
}

void updateOledStandby() {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    display.printf("--- %s ---\n", HUB_ID);
    display.println("STATUS: READY");
    display.println("Scan RFID Tag...");
    if (WiFi.status() == WL_CONNECTED) {
        display.println("WiFi: Connected");
    } else {
        display.println("WiFi: Offline");
    }
    display.display();
}

void loop() {
    // Scan for BLE advertisements from the active tag in background
    ble_tag_detected = false;
    pBLEScan->start(BLE_SCAN_TIME_SECONDS, false);
    pBLEScan->clearResults(); 
    
    // Check if RFID card is present
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
        Serial.println("\n[RFID] Card Scanned!");
        
        // Convert UID to string representation
        String rfid_uid = "";
        for (byte i = 0; i < mfrc522.uid.size; i++) {
            rfid_uid += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
            rfid_uid += String(mfrc522.uid.uidByte[i], HEX);
        }
        rfid_uid.toUpperCase();
        Serial.printf("RFID UID: %s\n", rfid_uid.c_str());
        
        // Read local temperature from DHT22 (fallback if BLE tag not scanned)
        float local_temp = dht.readTemperature();
        if (isnan(local_temp)) {
            local_temp = 23.5; // default fallback
        }
        
        // Determine values to send
        String final_parcel_id = "MED-104"; // Default demo parcel
        float final_temperature = local_temp;
        bool tamper_switch_triggered = (digitalRead(BUTTON_PIN) == LOW); // Button triggers tamper
        
        if (ble_tag_detected && (ble_parcel_id != "")) {
            final_parcel_id = ble_parcel_id;
            final_temperature = ble_temperature;
            tamper_switch_triggered = tamper_switch_triggered || ble_tamper;
        }
        
        // Execute POST scan event
        postScanEvent(final_parcel_id, rfid_uid, final_temperature, tamper_switch_triggered);
        
        // Halt RFID card reading
        mfrc522.PICC_HaltA();
        mfrc522.PCD_StopCrypto1();
        
        delay(2000); // Cooldown delay after a scan
        updateOledStandby();
    }
    
    // Check if the push button is pressed while standing by (simulate direct failure/overload)
    if (digitalRead(BUTTON_PIN) == LOW) {
        Serial.println("[Button] Push button pressed - triggering local notification");
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(WHITE);
        display.setCursor(0, 0);
        display.printf("--- %s ---\n", HUB_ID);
        display.println("BUTTON INJECTED:");
        display.println("Local Breach Alert");
        display.display();
        
        digitalWrite(RED_LED_PIN, HIGH);
        digitalWrite(BUZZER_PIN, HIGH);
        delay(1000);
        digitalWrite(RED_LED_PIN, LOW);
        digitalWrite(BUZZER_PIN, LOW);
        updateOledStandby();
    }
}

void postScanEvent(String parcel_id, String rfid_uid, float temp, bool tamper) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[WiFi] Offline. Cannot send HTTP scan request.");
        triggerLocalError("WiFi Disconnected");
        return;
    }
    
    HTTPClient http;
    http.begin(BACKEND_SCAN_URL);
    http.addHeader("Content-Type", "application/json");
    
    // Build JSON payload matching contract
    StaticJsonDocument<512> doc;
    doc["device_id"] = DEVICE_ID;
    doc["hub_id"] = HUB_ID;
    doc["parcel_id"] = parcel_id;
    doc["rfid_uid"] = rfid_uid;
    doc["qr_payload"] = "http://localhost:5173/scan/" + String(HUB_ID) + "?parcel_id=" + parcel_id;
    doc["temperature_c"] = temp;
    doc["button_pressed"] = tamper;
    
    // GPS coordinates (approx coordinates of HUB-A and HUB-B)
    if (IS_HUB_A) {
        doc["lat"] = 11.0168;
        doc["lng"] = 76.9558;
    } else {
        doc["lat"] = 11.0250;
        doc["lng"] = 76.9650;
    }
    
    doc["timestamp"] = "2026-06-08T15:00:00Z";
    
    // Add BLE tag scan details if detected
    if (ble_tag_detected) {
        doc["ble_verified"] = true;
        // RSSI-to-distance mapping approximation
        float ble_distance_m = pow(10, ((-59.0 - ble_rssi) / 20.0));
        doc["ble_rssi_m"] = ble_distance_m;
    } else {
        doc["ble_verified"] = false;
        doc["ble_rssi_m"] = 0.0;
    }
    
    // Add ESP-NOW direct handshake cache data (for HUB-B receiving)
    if (!IS_HUB_A && cached_prior_acceptance) {
        doc["esp_now_prior_acceptance"] = true;
        doc["esp_now_prior_hub"] = cached_prior_hub;
        doc["esp_now_prior_hub"] = cached_prior_hub;
        doc["esp_now_trust_delta"] = cached_trust_delta;
        
        // Reset cache after scan completes
        cached_prior_acceptance = false;
        cached_prior_hub = "";
        cached_trust_delta = 0.0;
    } else {
        doc["esp_now_prior_acceptance"] = false;
        doc["esp_now_prior_hub"] = "";
        doc["esp_now_trust_delta"] = 0.0;
    }
    
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    Serial.printf("[HTTP] POSTing payload: %s\n", jsonPayload.c_str());
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.printf("[HTTP] Response code: %d, Content: %s\n", httpResponseCode, response.c_str());
        
        StaticJsonDocument<512> responseDoc;
        DeserializationError err = deserializeJson(responseDoc, response);
        
        if (!err) {
            bool accepted = responseDoc["accepted"] | false;
            const char* led = responseDoc["led"] | "red";
            const char* message = responseDoc["message"] | "";
            const char* decision = responseDoc["decision"] | "";
            
            display.clearDisplay();
            display.setTextSize(1);
            display.setCursor(0, 0);
            display.printf("--- %s ---\n", HUB_ID);
            
            if (accepted) {
                // Flash GREEN LED
                digitalWrite(GREEN_LED_PIN, HIGH);
                digitalWrite(RED_LED_PIN, LOW);
                
                display.println("DECISION: ACCEPTED");
                display.printf("Parcel: %s\n", parcel_id.c_str());
                display.println("Proof-of-Movement OK");
                display.display();
                
                // Beep once for success
                digitalWrite(BUZZER_PIN, HIGH);
                delay(150);
                digitalWrite(BUZZER_PIN, LOW);
                
                // If this is HUB-A, send ESP-NOW accepted handshake to HUB-B
                if (IS_HUB_A) {
                    struct_message sendMsg;
                    strcpy(sendMsg.parcel_id, parcel_id.c_str());
                    strcpy(sendMsg.msg_type, "HUB_ACCEPTED");
                    sendMsg.trust_delta = 0.01;
                    
                    Serial.printf("[ESP-NOW] Sending HUB_ACCEPTED to HUB-B for %s\n", parcel_id.c_str());
                    esp_now_send(PEER_MAC, (uint8_t *) &sendMsg, sizeof(sendMsg));
                    
                    // Log the ESP-NOW handshake to the backend for auditing
                    postP2PHandshake("HUB-A", "HUB-B", parcel_id, "HUB_ACCEPTED", 0.01);
                }
            } else {
                // Flash RED LED
                digitalWrite(GREEN_LED_PIN, LOW);
                digitalWrite(RED_LED_PIN, HIGH);
                
                display.printf("DECISION: %s\n", decision);
                display.println("ANOMALY BLOCKED!");
                display.display();
                
                // Triple warning beep
                for(int i=0; i<3; i++) {
                    digitalWrite(BUZZER_PIN, HIGH);
                    delay(80);
                    digitalWrite(BUZZER_PIN, LOW);
                    delay(80);
                }
            }
            
            delay(1500);
            digitalWrite(GREEN_LED_PIN, LOW);
            digitalWrite(RED_LED_PIN, LOW);
        } else {
            triggerLocalError("JSON Parse Error");
        }
    } else {
        Serial.printf("[HTTP] POST failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
        triggerLocalError("Server Unreachable");
    }
    http.end();
}

void postP2PHandshake(String sender, String receiver, String parcel_id, String msg_type, float delta) {
    HTTPClient http;
    http.begin(BACKEND_P2P_URL);
    http.addHeader("Content-Type", "application/json");
    
    StaticJsonDocument<256> doc;
    doc["sender_hub"] = sender;
    doc["receiver_hub"] = receiver;
    doc["parcel_id"] = parcel_id;
    doc["message_type"] = msg_type;
    doc["trust_delta"] = delta;
    
    String jsonPayload;
    serializeJson(doc, jsonPayload);
    
    Serial.printf("[HTTP] Logging P2P Handshake: %s\n", jsonPayload.c_str());
    int httpResponseCode = http.POST(jsonPayload);
    Serial.printf("[HTTP] Handshake log response: %d\n", httpResponseCode);
    http.end();
}

void triggerLocalError(String msg) {
    digitalWrite(GREEN_LED_PIN, LOW);
    digitalWrite(RED_LED_PIN, HIGH);
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.printf("--- %s ---\n", HUB_ID);
    display.println("ERROR:");
    display.println(msg.c_str());
    display.display();
    
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(1000);
    digitalWrite(RED_LED_PIN, LOW);
}
