#!/bin/bash
# Phase 9 smoke test script for PacketFlow ImmuneNet Backend

BACKEND_URL="http://localhost:8000"
FAILED=0

echo "=== PACKETFLOW IMMUNENET BACKEND SMOKE TEST ==="

# Helper to check GET endpoints
check_get() {
    local path=$1
    local name=$2
    local expected_code=200
    if [ ! -z "$3" ]; then
        expected_code=$3
    fi
    
    echo -n "Checking GET ${path} (${name})... "
    code=$(curl -s -o /dev/null -w "%{http_code}" "${BACKEND_URL}${path}")
    if [ "$code" -eq "$expected_code" ]; then
        echo "PASS (HTTP ${code})"
    else
        echo "FAIL (HTTP ${code}, expected ${expected_code})"
        FAILED=1
    fi
}

# Helper to check POST endpoints
check_post() {
    local path=$1
    local name=$2
    local data=$3
    local expected_code=200
    if [ ! -z "$4" ]; then
        expected_code=$4
    fi

    echo -n "Checking POST ${path} (${name})... "
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "Content-Type: application/json" -d "${data}" "${BACKEND_URL}${path}")
    if [ "$code" -eq "$expected_code" ]; then
        echo "PASS (HTTP ${code})"
    else
        echo "FAIL (HTTP ${code}, expected ${expected_code})"
        FAILED=1
    fi
}

# 1. GET /health
check_get "/health" "Health check"

# 2. POST /demo/reset
check_post "/demo/reset" "Demo reset" "{}"

# 3. GET /ready
check_get "/ready" "Ready check"

# 4. POST /route/next-hop
check_post "/route/next-hop" "Route next-hop" '{"parcel_id": "MED-104", "current_hub": "HUB-A", "destination_hub": "CUSTOMER-ZONE"}'

# 5. POST /scan (valid at HUB-A)
check_post "/scan" "Valid scan at HUB-A" '{"parcel_id": "MED-104", "hub_id": "HUB-A", "scanner_id": "SCANNER-07", "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18}, "temperature_c": 24.3, "carrier_type": "van", "tamper": false}'

# 6. POST /scan/fake
check_post "/scan/fake" "Fake scan" '{"parcel_id": "MED-104", "claimed_hub": "HUB-C", "fake_gps": {"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20}}'

# 7. POST /scenario/overload-hub
check_post "/scenario/overload-hub" "Overload HUB-B" '{"parcel_id": "MED-104", "hub_id": "HUB-B", "congestion": 0.90}'

# 8. POST /hardware/p2p-handshake
check_post "/hardware/p2p-handshake" "Hardware P2P handshake" '{"sender_hub": "HUB-A", "receiver_hub": "HUB-B", "parcel_id": "MED-104", "message_type": "TRUST_SYNC", "trust_delta": 0.02, "eta_sec": 300}'

# 9. POST /hardware/scan
check_post "/hardware/scan" "Hardware scan" '{"parcel_id": "MED-104", "hub_id": "HUB-A", "scanner_id": "ESP32-HUB-A", "rfid_verified": true, "temperature_c": 24.3, "tamper": false, "gps": {"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18}}'

# 10. GET /metrics
check_get "/metrics" "Metrics"

# 11. GET /ledger/events
check_get "/ledger/events" "Ledger events"

# 12. POST /demo/validate
check_post "/demo/validate" "Demo validation" "{}"

echo "=== SMOKE TEST SUMMARY ==="
if [ "$FAILED" -eq 0 ]; then
    echo "ALL TESTS PASSED SUCCESSFULLY!"
    exit 0
else
    echo "SOME TESTS FAILED! PLEASE CHECK LOGS."
    exit 1
fi
