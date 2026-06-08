#pragma once

// Set to true to compile for HUB-A, or false to compile for HUB-B
#define IS_HUB_A true

// Wi-Fi Configuration (Wokwi-GUEST is default for Wokwi simulation)
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// Backend Endpoints
// Assuming the backend is running on localhost, we point to the host IP. 
// For Wokwi simulation, use your computer's local network IP (e.g. 192.168.1.X)
#define BACKEND_BASE_URL "http://192.168.1.100:8000"
#define BACKEND_SCAN_URL BACKEND_BASE_URL "/hardware/scan"
#define BACKEND_P2P_URL BACKEND_BASE_URL "/hardware/p2p-handshake"

// ESP-NOW Configuration
// Replace with the physical MAC address of the OTHER node.
// To find MAC: Open Serial Monitor on boot. It will print the local MAC address.
#if IS_HUB_A
  // MAC address of HUB-B
  static uint8_t PEER_MAC[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x02};
#else
  // MAC address of HUB-A
  static uint8_t PEER_MAC[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x01};
#endif
