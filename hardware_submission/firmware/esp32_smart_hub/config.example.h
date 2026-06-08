#pragma once

// Set to true to compile for HUB-A, or false to compile for HUB-B
#define IS_HUB_A true

#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define BACKEND_BASE_URL "http://192.168.1.100:8000"
#define BACKEND_SCAN_URL BACKEND_BASE_URL "/hardware/scan"
#define BACKEND_P2P_URL BACKEND_BASE_URL "/hardware/p2p-handshake"

#if IS_HUB_A
  static uint8_t PEER_MAC[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x02};
#else
  static uint8_t PEER_MAC[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x01};
#endif
