# Owner: Person 3 — Hardware + Demo + Presentation Lead
# Purpose: Interactive ASCII hardware simulation of the Smart Hubs and Parcel Tag using ESP32-C3 v2 architecture.
# No external dependencies needed. Run with: python simulate_hardware.py

import json
import urllib.request
import urllib.error
import time
import os
import sys
import io

# Force UTF-8 stdout to support box-drawing characters on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
from collections import deque

# Configuration matching config.h & backend routes
BACKEND_BASE_URL = "http://localhost:8000"
SCAN_ENDPOINT = BACKEND_BASE_URL + "/hardware/scan"
P2P_ENDPOINT = BACKEND_BASE_URL + "/hardware/p2p-handshake"
RESET_ENDPOINT = BACKEND_BASE_URL + "/demo/reset"

# Simulator State
tag_parcel_id = "MED-104"
tag_temp = 24.3
tag_tamper = False
tag_battery_v = 4.2  # Max charge 4.2V

# Hub A (Central Node) State
hub_a_oled = [
    "--- HUB-A ---",
    "STATUS: READY",
    "Scan RFID Tag..."
]
hub_a_green = False
hub_a_red = False
hub_a_buzzer = "OFF"
hub_a_rfid_uid = "04A8B9C104"

# Hub B (Relay Node) State
hub_b_oled = [
    "--- HUB-B ---",
    "STATUS: READY",
    "Scan RFID Tag..."
]
hub_b_green = False
hub_b_red = False
hub_b_buzzer = "OFF"
hub_b_rfid_uid = "04A8B9C104"

# ESP-NOW Cache for Hub B
hub_b_cache_acceptance = False
hub_b_cache_hub = ""
hub_b_cache_delta = 0.0

# Network Monitoring State
last_esp_now_message = "No messages sent"
last_backend_response = "No requests sent"

# Live Serial Log Queue (stores last 6 logs)
serial_logs = deque([
    "[SYSTEM] ESP32-C3 Hardware Simulation Started.",
    "[SYSTEM] Ready. Select options [1-2, T, +, -, R] to interact."
], maxlen=6)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def log_serial(msg):
    timestamp = time.strftime("%H:%M:%S")
    serial_logs.append(f"[{timestamp}] {msg}")

def make_post_request(url, data):
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    jsondata = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req, jsondata, timeout=3) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        return 0, {"error": str(e.reason)}
    except Exception as e:
        return 0, {"error": str(e)}

def get_ble_adv_name():
    # BLE name format: P_[ParcelID_no_hyphen]_[Temp]_[TamperInt]
    # Example: P_MED104_24.3_0
    clean_id = tag_parcel_id.replace("-", "")
    tamper_val = 1 if tag_tamper else 0
    return f"P_{clean_id}_{tag_temp:.1f}_{tamper_val}"

def draw_interface():
    clear_screen()
    
    # ANSI Colors
    C_BLUE = "\033[94m"
    C_GREEN = "\033[92m"
    C_RED = "\033[91m"
    C_YELLOW = "\033[93m"
    C_CYAN = "\033[96m"
    C_GRAY = "\033[90m"
    C_BOLD = "\033[1m"
    C_RESET = "\033[0m"
    
    # Header Banner
    print(C_BLUE + C_BOLD + "┌──────────────────────────────────────────────────────────────────────────────┐")
    print("│             PACKETFLOW IMMUNENET v2 HARDWARE MESH SIMULATOR                  │")
    print("│                    MCU: ESP32-C3-DevKitM-1 SHIELD ARCHITECTURE               │")
    print("└──────────────────────────────────────────────────────────────────────────────┘" + C_RESET)
    
    # Column 1: Active Tag & MESH Info
    tamper_status = C_RED + C_BOLD + "BREACHED" + C_RESET if tag_tamper else C_GREEN + "SECURE" + C_RESET
    temp_color = C_RED + C_BOLD if tag_temp >= 25.0 else C_GREEN
    ble_packet = get_ble_adv_name()
    
    print(C_BOLD + " [ ACTIVE SMART PARCEL TAG (ESP32-C3) ]" + C_RESET + "    " + C_BOLD + " [ MESH METER & BLE STATUS ]" + C_RESET)
    print(f" ├─ Parcel ID : {C_CYAN}{tag_parcel_id:<14}{C_RESET}             ├─ BLE Adv Packet : {C_YELLOW}{ble_packet:<20}{C_RESET}")
    print(f" ├─ Temp      : {temp_color}{tag_temp:>4.1f} °C{C_RESET} (Limit 25C)       ├─ ESP-NOW Peer A : {C_GRAY}7C:DF:A1:A2:B3:C0 (Hub A){C_RESET}")
    print(f" ├─ Tamper    : {tamper_status:<16}             ├─ ESP-NOW Peer B : {C_GRAY}7C:DF:A1:A2:B3:C4 (Hub B){C_RESET}")
    print(f" ├─ Battery   : {C_GREEN}{tag_battery_v:.2f} V{C_RESET} [100%]             ├─ ESP-NOW Message: {C_CYAN}{last_esp_now_message[:30]}{C_RESET}")
    print(f" └─ DHT22 Pin : {C_GRAY}Pad 7 (GPIO 10){C_RESET}               └─ MESH Connection: {C_GREEN}ONLINE / ACTIVE{C_RESET}")
    print(C_GRAY + "─" * 80 + C_RESET)
    
    # Hub OLED formatting
    ha_l1 = hub_a_oled[0] if len(hub_a_oled) > 0 else ""
    ha_l2 = hub_a_oled[1] if len(hub_a_oled) > 1 else ""
    ha_l3 = hub_a_oled[2] if len(hub_a_oled) > 2 else ""
    
    hb_l1 = hub_b_oled[0] if len(hub_b_oled) > 0 else ""
    hb_l2 = hub_b_oled[1] if len(hub_b_oled) > 1 else ""
    hb_l3 = hub_b_oled[2] if len(hub_b_oled) > 2 else ""
    
    # LEDs and Buzzer status strings
    ha_green_led = C_GREEN + C_BOLD + "●" + C_RESET if hub_a_green else C_GRAY + "○" + C_RESET
    ha_red_led = C_RED + C_BOLD + "●" + C_RESET if hub_a_red else C_GRAY + "○" + C_RESET
    hb_green_led = C_GREEN + C_BOLD + "●" + C_RESET if hub_b_green else C_GRAY + "○" + C_RESET
    hb_red_led = C_RED + C_BOLD + "●" + C_RESET if hub_b_red else C_GRAY + "○" + C_RESET
    
    ha_buz = C_YELLOW + C_BOLD + hub_a_buzzer + C_RESET if hub_a_buzzer != "OFF" else C_GRAY + "OFF" + C_RESET
    hb_buz = C_YELLOW + C_BOLD + hub_b_buzzer + C_RESET if hub_b_buzzer != "OFF" else C_GRAY + "OFF" + C_RESET
    
    # Print Hub panels side-by-side
    print("         " + C_BLUE + C_BOLD + "┌─────────────────────────────────────┐" + C_RESET + "         " + C_BLUE + C_BOLD + "┌─────────────────────────────────────┐" + C_RESET)
    print("         " + C_BLUE + C_BOLD + "│        SMART HUB A: CENTRAL         │" + C_RESET + "         " + C_BLUE + C_BOLD + "│         SMART HUB B: RELAY          │" + C_RESET)
    print("         " + C_BLUE + C_BOLD + "├─────────────────────────────────────┤" + C_RESET + "         " + C_BLUE + C_BOLD + "├─────────────────────────────────────┤" + C_RESET)
    print("         │  " + C_BOLD + "OLED DISPLAY:" + C_RESET + "                     │         │  " + C_BOLD + "OLED DISPLAY:" + C_RESET + "                     │")
    print(f"         │  {C_YELLOW}┌───────────────────────────────┐{C_RESET}  │         │  {C_YELLOW}┌───────────────────────────────┐{C_RESET}  │")
    print(f"         │  │ {C_BOLD}{ha_l1:<29}{C_RESET} │  │         │  │ {C_BOLD}{hb_l1:<29}{C_RESET} │  │")
    print(f"         │  │ {ha_l2:<29} │  │         │  │ {hb_l2:<29} │  │")
    print(f"         │  │ {ha_l3:<29} │  │         │  │ {hb_l3:<29} │  │")
    print(f"         │  {C_YELLOW}└───────────────────────────────┘{C_RESET}  │         │  {C_YELLOW}└───────────────────────────────┘{C_RESET}  │")
    print(f"         │  LEDs  : Green [{ha_green_led}]  Red [{ha_red_led}]        │         │  LEDs  : Green [{hb_green_led}]  Red [{hb_red_led}]        │")
    print(f"         │  Buzzer: {ha_buz:<25} │         │  Buzzer: {hb_buz:<25} │")
    print(f"         │  RFID  : {C_GRAY}Pad 9/11 ({hub_a_rfid_uid}){C_RESET}        │         │  RFID  : {C_GRAY}Pad 9/11 ({hub_b_rfid_uid}){C_RESET}        │")
    print(f"         │  OLED  : {C_GRAY}Pad 2/3 (I2C SDA/SCL){C_RESET}     │         │  OLED  : {C_GRAY}Pad 2/3 (I2C SDA/SCL){C_RESET}     │")
    print("         " + C_BLUE + C_BOLD + "└─────────────────────────────────────┘" + C_RESET + "         " + C_BLUE + C_BOLD + "└─────────────────────────────────────┘" + C_RESET)
    print(f" Backend HTTP Logs: {C_CYAN}{last_backend_response}{C_RESET}")
    print(C_GRAY + "─" * 80 + C_RESET)
    
    # Live Serial logs console
    print(C_BOLD + " [ LIVE MCU HARDWARE LOGS - SERIAL TERMINAL ]" + C_RESET)
    for log in list(serial_logs):
        if "[ERROR]" in log or "ANOMALY" in log or "Failed" in log:
            print(f"  {C_RED}{log}{C_RESET}")
        elif "ACCEPTED" in log or "OK" in log or "successfully" in log:
            print(f"  {C_GREEN}{log}{C_RESET}")
        elif "ESP-NOW" in log or "BLE" in log:
            print(f"  {C_CYAN}{log}{C_RESET}")
        else:
            print(f"  {log}")
    print(C_GRAY + "─" * 80 + C_RESET)
    
    # Command menu
    print(C_BOLD + "Controls:" + C_RESET)
    print(f"  [{C_GREEN}1{C_RESET}] Scan Tag at HUB-A                  [{C_GREEN}2{C_RESET}] Scan Tag at HUB-B")
    print(f"  [{C_CYAN}T{C_RESET}] Toggle Tag Tamper Switch           [{C_CYAN}+{C_RESET}] Increase Temp    [{C_CYAN}-{C_RESET}] Decrease Temp")
    print(f"  [{C_CYAN}P{C_RESET}] Edit custom Parcel ID              [{C_CYAN}U{C_RESET}] Edit custom RFID UID")
    print(f"  [{C_RED}R{C_RESET}] Reset Database Demo State          [{C_RED}Q{C_RESET}] Quit / Exit")
    print(C_BLUE + "================================================================================" + C_RESET)

def run_spinner(text, duration=1.0):
    C_CYAN = "\033[96m"
    C_RESET = "\033[0m"
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    steps = int(duration * 10)
    for i in range(steps):
        sys.stdout.write(f"\r  {C_CYAN}{spinner[i % len(spinner)]} {text}...{C_RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(text) + 20) + "\r")
    sys.stdout.flush()

def simulate_scan_hub_a():
    global hub_a_oled, hub_a_green, hub_a_red, hub_a_buzzer, last_backend_response, last_esp_now_message
    global hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta, hub_b_oled
    
    hub_a_oled = ["--- HUB-A ---", "CONNECTING...", "Querying Server..."]
    draw_interface()
    
    log_serial(f"[RFID] RC522 scanned card, UID: {hub_a_rfid_uid}")
    run_spinner("Polling local DHT22 and scanning BLE advertising beacons", 0.8)
    
    ble_name = get_ble_adv_name()
    log_serial(f"[BLE] Scanning BLE packets... Active Tag detected: {ble_name}")
    log_serial(f"[BLE] Verification RSSI: -55dBm (~0.63m distance estimate)")
    
    run_spinner("POSTing hardware Scan Payload to /hardware/scan", 0.6)
    
    payload = {
        "device_id": "ESP32-HUB-A-01",
        "hub_id": "HUB-A",
        "parcel_id": tag_parcel_id,
        "rfid_uid": hub_a_rfid_uid,
        "qr_payload": f"http://localhost:5173/scan/HUB-A?parcel_id={tag_parcel_id}",
        "temperature_c": tag_temp,
        "button_pressed": tag_tamper,
        "lat": 11.0168,
        "lng": 76.9558,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ble_verified": True,
        "ble_rssi_m": 0.63,
        "esp_now_prior_acceptance": False,
        "esp_now_prior_hub": "",
        "esp_now_trust_delta": 0.0
    }
    
    code, res = make_post_request(SCAN_ENDPOINT, payload)
    
    if code == 200:
        accepted = res.get("accepted", False)
        msg = res.get("message", "")
        decision = res.get("decision", "blocked").upper()
        
        last_backend_response = f"HTTP 200 - {decision}: {msg}"
        
        if accepted:
            hub_a_green = True
            hub_a_red = False
            hub_a_buzzer = "1x SHORT BEEP"
            hub_a_oled = [
                "DECISION: ACCEPTED",
                f"Parcel: {tag_parcel_id}",
                "Proof-of-Movement OK"
            ]
            log_serial(f"[HTTP] Hub-A scan ACCEPTED: {msg}")
            
            # Simulate ESP-NOW transmit to HUB-B
            run_spinner("ESP-NOW: Broadcast accepted message to Hub-B peer mesh", 0.5)
            last_esp_now_message = f"HUB_ACCEPTED for {tag_parcel_id} (Delta: 0.01)"
            log_serial(f"[ESP-NOW] Broadcast payload sent to Peer B (7C:DF:A1:A2:B3:C4)")
            
            hub_b_cache_acceptance = True
            hub_b_cache_hub = "HUB-A"
            hub_b_cache_delta = 0.01
            hub_b_oled = [
                "STATUS: INCOMING",
                f"Parcel: {tag_parcel_id}",
                "From Peer: HUB-A"
            ]
            log_serial(f"[ESP-NOW] Peer Hub B received accepted message. Cached payload.")
            
            # Post P2P handshake log
            p2p_payload = {
                "sender_hub": "HUB-A",
                "receiver_hub": "HUB-B",
                "parcel_id": tag_parcel_id,
                "message_type": "HUB_ACCEPTED",
                "trust_delta": 0.01
            }
            make_post_request(P2P_ENDPOINT, p2p_payload)
        else:
            hub_a_green = False
            hub_a_red = True
            hub_a_buzzer = "3x WARNING BEEPS"
            hub_a_oled = [
                f"DECISION: {decision}",
                "ANOMALY BLOCKED!",
                f"{msg[:30]}"
            ]
            log_serial(f"[ERROR] Hub-A scan BLOCKED: Anomaly detected! Reason: {msg}")
    else:
        last_backend_response = f"HTTP Error - {res.get('error', 'Unknown Error')}"
        hub_a_green = False
        hub_a_red = True
        hub_a_buzzer = "1x LONG ALARM BEEP"
        hub_a_oled = [
            "ERROR:",
            "Server Unreachable",
            "Verify backend port 8000"
        ]
        log_serial(f"[ERROR] HTTP request failed. Server offline or unreachable.")
        
    draw_interface()
    time.sleep(2.5)
    hub_a_green = False
    hub_a_red = False
    hub_a_buzzer = "OFF"
    hub_a_oled = [
        "--- HUB-A ---",
        "STATUS: READY",
        "Scan RFID Tag..."
    ]
    draw_interface()

def simulate_scan_hub_b():
    global hub_b_oled, hub_b_green, hub_b_red, hub_b_buzzer, last_backend_response
    global hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta
    
    hub_b_oled = ["--- HUB-B ---", "CONNECTING...", "Querying Server..."]
    draw_interface()
    
    log_serial(f"[RFID] RC522 scanned card, UID: {hub_b_rfid_uid}")
    run_spinner("Polling local DHT22 and scanning BLE advertising beacons", 0.8)
    
    ble_name = get_ble_adv_name()
    log_serial(f"[BLE] Scanning BLE packets... Active Tag detected: {ble_name}")
    log_serial(f"[BLE] Verification RSSI: -65dBm (~1.99m distance estimate)")
    
    if hub_b_cache_acceptance:
        log_serial(f"[ESP-NOW] Local cache check: Peer A accepted message found. Injecting to payload.")
    else:
        log_serial(f"[ESP-NOW] Local cache check: No peer mesh messages cached.")
        
    run_spinner("POSTing hardware Scan Payload to /hardware/scan", 0.6)
    
    payload = {
        "device_id": "ESP32-HUB-B-01",
        "hub_id": "HUB-B",
        "parcel_id": tag_parcel_id,
        "rfid_uid": hub_b_rfid_uid,
        "qr_payload": f"http://localhost:5173/scan/HUB-B?parcel_id={tag_parcel_id}",
        "temperature_c": tag_temp,
        "button_pressed": tag_tamper,
        "lat": 11.0250,
        "lng": 76.9650,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ble_verified": True,
        "ble_rssi_m": 1.99,
        "esp_now_prior_acceptance": hub_b_cache_acceptance,
        "esp_now_prior_hub": hub_b_cache_hub if hub_b_cache_acceptance else "",
        "esp_now_trust_delta": hub_b_cache_delta if hub_b_cache_acceptance else 0.0
    }
    
    # Clear local ESP-NOW cache
    hub_b_cache_acceptance = False
    hub_b_cache_hub = ""
    hub_b_cache_delta = 0.0
    
    code, res = make_post_request(SCAN_ENDPOINT, payload)
    
    if code == 200:
        accepted = res.get("accepted", False)
        msg = res.get("message", "")
        decision = res.get("decision", "blocked").upper()
        
        last_backend_response = f"HTTP 200 - {decision}: {msg}"
        
        if accepted:
            hub_b_green = True
            hub_b_red = False
            hub_b_buzzer = "1x SHORT BEEP"
            hub_b_oled = [
                "DECISION: ACCEPTED",
                f"Parcel: {tag_parcel_id}",
                "Proof-of-Movement OK"
            ]
            log_serial(f"[HTTP] Hub-B scan ACCEPTED: {msg}")
        else:
            hub_b_green = False
            hub_b_red = True
            hub_b_buzzer = "3x WARNING BEEPS"
            hub_b_oled = [
                f"DECISION: {decision}",
                "ANOMALY BLOCKED!",
                f"{msg[:30]}"
            ]
            log_serial(f"[ERROR] Hub-B scan BLOCKED: Anomaly detected! Reason: {msg}")
    else:
        last_backend_response = f"HTTP Error - {res.get('error', 'Unknown Error')}"
        hub_b_green = False
        hub_b_red = True
        hub_b_buzzer = "1x LONG ALARM BEEP"
        hub_b_oled = [
            "ERROR:",
            "Server Unreachable",
            "Verify backend port 8000"
        ]
        log_serial(f"[ERROR] HTTP request failed. Server offline or unreachable.")
        
    draw_interface()
    time.sleep(2.5)
    hub_b_green = False
    hub_b_red = False
    hub_b_buzzer = "OFF"
    hub_b_oled = [
        "--- HUB-B ---",
        "STATUS: READY",
        "Scan RFID Tag..."
    ]
    draw_interface()

def reset_demo():
    global last_backend_response, tag_temp, tag_tamper, hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta
    global hub_a_oled, hub_b_oled, last_esp_now_message
    
    run_spinner("Resetting demo state on FastAPI backend database", 1.0)
    code, res = make_post_request(RESET_ENDPOINT, {})
    if code == 200:
        last_backend_response = "HTTP 200 - Demo Reset Successful"
        log_serial("[RESET] Database demo state refreshed successfully.")
    else:
        last_backend_response = f"HTTP Error - Reset Failed: {res.get('error', 'Unknown Error')}"
        log_serial("[ERROR] Database demo state reset failed.")
        
    tag_temp = 24.3
    tag_tamper = False
    hub_b_cache_acceptance = False
    hub_b_cache_hub = ""
    hub_b_cache_delta = 0.0
    last_esp_now_message = "No messages sent (Reset)"
    hub_a_oled = [
        "--- HUB-A ---",
        "STATUS: READY",
        "Scan RFID Tag..."
    ]
    hub_b_oled = [
        "--- HUB-B ---",
        "STATUS: READY",
        "Scan RFID Tag..."
    ]
    draw_interface()

def main():
    global tag_tamper, tag_temp, tag_parcel_id, hub_a_rfid_uid, hub_b_rfid_uid
    
    # Configure UTF-8 encoding on Windows consoles
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
        
    while True:
        draw_interface()
        try:
            cmd = input("Command >> ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting simulator.")
            sys.exit(0)
            
        if cmd == '1':
            simulate_scan_hub_a()
        elif cmd == '2':
            simulate_scan_hub_b()
        elif cmd == 'T':
            tag_tamper = not tag_tamper
            log_serial(f"[TAG] Tamper limit switch toggled. State: {'TAMPERED' if tag_tamper else 'SECURE'}")
        elif cmd == '+':
            tag_temp += 0.5
            log_serial(f"[TAG] Temp increased to {tag_temp:.1f} °C")
        elif cmd == '-':
            tag_temp -= 0.5
            log_serial(f"[TAG] Temp decreased to {tag_temp:.1f} °C")
        elif cmd == 'P':
            new_id = input("Enter custom Parcel ID (e.g. MED-104) >> ").strip()
            if new_id:
                tag_parcel_id = new_id
                log_serial(f"[TAG] Parcel ID updated to: {tag_parcel_id}")
        elif cmd == 'U':
            new_uid = input("Enter custom RFID Card UID >> ").strip()
            if new_uid:
                hub_a_rfid_uid = new_uid
                hub_b_rfid_uid = new_uid
                log_serial(f"[RFID] Card UID configured to: {new_uid}")
        elif cmd == 'R':
            reset_demo()
        elif cmd == 'Q':
            print("Exiting simulator.")
            break
        else:
            print("Invalid Option. Press Enter to retry...")
            time.sleep(1)

if __name__ == '__main__':
    main()
