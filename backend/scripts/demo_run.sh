#!/bin/bash
# Phase 9 main demo run script for PacketFlow ImmuneNet Backend

BACKEND_URL="http://localhost:8000"

echo "=== STARTING PACKETFLOW IMMUNENET DEMO SEQUENCE ==="

# 1. Reset demo
echo "1. Resetting demo state..."
curl -s -X POST "${BACKEND_URL}/demo/reset" | json_pp || curl -s -X POST "${BACKEND_URL}/demo/reset"
echo -e "\n--------------------------------------------------"

# 2. Fetching initial route
echo "2. Fetching initial route for MED-104..."
curl -s -X POST "${BACKEND_URL}/route/next-hop" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "current_hub": "HUB-A", "destination_hub": "CUSTOMER-ZONE"}' | json_pp || curl -s -X POST "${BACKEND_URL}/route/next-hop" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "current_hub": "HUB-A", "destination_hub": "CUSTOMER-ZONE"}'
echo -e "\n--------------------------------------------------"

# 3. Valid scan at HUB-A
echo "3. Submitting valid scan at HUB-A..."
curl -s -X POST "${BACKEND_URL}/scan" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "hub_id": "HUB-A", "scanner_id": "SCANNER-07", "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18}, "temperature_c": 24.3, "carrier_type": "van", "tamper": false}' | json_pp || curl -s -X POST "${BACKEND_URL}/scan" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "hub_id": "HUB-A", "scanner_id": "SCANNER-07", "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18}, "temperature_c": 24.3, "carrier_type": "van", "tamper": false}'
echo -e "\n--------------------------------------------------"

# 4. Hardware p2p handshake HUB-A -> HUB-B
echo "4. Simulating hardware P2P handshake HUB-A -> HUB-B..."
curl -s -X POST "${BACKEND_URL}/hardware/p2p-handshake" \
  -H "Content-Type: application/json" \
  -d '{"sender_hub": "HUB-A", "receiver_hub": "HUB-B", "parcel_id": "MED-104", "message_type": "TRUST_SYNC", "trust_delta": 0.02, "eta_sec": 300}' | json_pp || curl -s -X POST "${BACKEND_URL}/hardware/p2p-handshake" -H "Content-Type: application/json" -d '{"sender_hub": "HUB-A", "receiver_hub": "HUB-B", "parcel_id": "MED-104", "message_type": "TRUST_SYNC", "trust_delta": 0.02, "eta_sec": 300}'
echo -e "\n--------------------------------------------------"

# 5. Hardware scan at HUB-B with esp_now_prior_acceptance
echo "5. Simulating hardware scan at HUB-B with prior acceptance..."
curl -s -X POST "${BACKEND_URL}/hardware/scan" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "hub_id": "HUB-B", "scanner_id": "ESP32-HUB-B", "rfid_verified": true, "temperature_c": 24.1, "tamper": false, "esp_now_prior_acceptance": true, "esp_now_prior_hub": "HUB-A", "esp_now_trust_delta": 0.02, "gps": {"lat": 11.0250, "lng": 76.9650, "accuracy_m": 15}}' | json_pp || curl -s -X POST "${BACKEND_URL}/hardware/scan" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "hub_id": "HUB-B", "scanner_id": "ESP32-HUB-B", "rfid_verified": true, "temperature_c": 24.1, "tamper": false, "esp_now_prior_acceptance": true, "esp_now_prior_hub": "HUB-A", "esp_now_trust_delta": 0.02, "gps": {"lat": 11.0250, "lng": 76.9650, "accuracy_m": 15}}'
echo -e "\n--------------------------------------------------"

# 6. Overload HUB-B
echo "6. Overloading HUB-B..."
curl -s -X POST "${BACKEND_URL}/scenario/overload-hub" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "hub_id": "HUB-B", "congestion": 0.95}' | json_pp || curl -s -X POST "${BACKEND_URL}/scenario/overload-hub" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "hub_id": "HUB-B", "congestion": 0.95}'
echo -e "\n--------------------------------------------------"

# 7. Fake scan at HUB-C
echo "7. Simulating fake scan at HUB-C..."
curl -s -X POST "${BACKEND_URL}/scan/fake" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "claimed_hub": "HUB-C", "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20}}' | json_pp || curl -s -X POST "${BACKEND_URL}/scan/fake" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "claimed_hub": "HUB-C", "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20}}'
echo -e "\n--------------------------------------------------"

# 8. Temperature breach
echo "8. Triggering temperature breach..."
curl -s -X POST "${BACKEND_URL}/scenario/temp-breach" \
  -H "Content-Type: application/json" \
  -d '{"parcel_id": "MED-104", "hub_id": "HUB-A", "temperature_c": 29.5}' | json_pp || curl -s -X POST "${BACKEND_URL}/scenario/temp-breach" -H "Content-Type: application/json" -d '{"parcel_id": "MED-104", "hub_id": "HUB-A", "temperature_c": 29.5}'
echo -e "\n--------------------------------------------------"

# 9. Print metrics
echo "9. Fetching final metrics..."
curl -s "${BACKEND_URL}/metrics" | json_pp || curl -s "${BACKEND_URL}/metrics"
echo -e "\n--------------------------------------------------"

# 10. Print ledger
echo "10. Fetching ledger events (recent 10)..."
curl -s "${BACKEND_URL}/ledger/events?limit=10" | json_pp || curl -s "${BACKEND_URL}/ledger/events?limit=10"
echo -e "\n--------------------------------------------------"

echo "=== DEMO SEQUENCE COMPLETED ==="
