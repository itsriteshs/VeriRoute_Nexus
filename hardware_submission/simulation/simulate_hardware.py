# Owner: Person 3 — Hardware + Demo + Presentation Lead
# Purpose: Interactive ASCII hardware simulation of the Smart Hubs and Parcel Tag.
# No external dependencies needed (uses standard urllib). Run with: python simulate_hardware.py

import json
import urllib.request
import urllib.error
import time
import os
import sys

# Configuration matching config.h
BACKEND_BASE_URL = "http://localhost:8000"
SCAN_ENDPOINT = BACKEND_BASE_URL + "/hardware/scan"
P2P_ENDPOINT = BACKEND_BASE_URL + "/hardware/p2p-handshake"
RESET_ENDPOINT = BACKEND_BASE_URL + "/demo/reset"

# Simulator State
tag_parcel_id = "MED-104"
tag_temp = 24.3
tag_tamper = False

hub_a_oled = "HUB-A STATUS: READY\nScan RFID Tag to verify..."
hub_a_green = False
hub_a_red = False
hub_a_buzzer = "OFF"

hub_b_oled = "HUB-B STATUS: READY\nScan RFID Tag to verify..."
hub_b_green = False
hub_b_red = False
hub_b_buzzer = "OFF"

# ESP-NOW Cache for Hub B
hub_b_cache_acceptance = False
hub_b_cache_hub = ""
hub_b_cache_delta = 0.0

last_esp_now_message = "No messages sent"
last_backend_response = "No requests sent"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def draw_interface():
    clear_screen()
    print("================================================================================")
    print("                      PACKETFLOW IMMUNENET HARDWARE SIMULATOR                   ")
    print("================================================================================")
    
    # Active Tag details
    tamper_status = "\033[91mTAMPERED\033[0m" if tag_tamper else "\033[92mSECURE\033[0m"
    temp_color = "\033[91m" if tag_temp >= 25.0 else "\033[92m"
    print(f"[ ACTIVE SMART PARCEL TAG ]             [ ESP-NOW MESH STATUS ]")
    print(f"Parcel ID: {tag_parcel_id}                      Last Message: {last_esp_now_message}")
    print(f"Temperature: {temp_color}{tag_temp:.1f} °C\033[0m (Limit 25C)        ESP-NOW Link: ACTIVE")
    print(f"Tamper Switch: {tamper_status}")
    print("--------------------------------------------------------------------------------")
    
    # Hub A OLED lines
    ha_lines = hub_a_oled.split('\n')
    ha_l1 = ha_lines[0] if len(ha_lines) > 0 else ""
    ha_l2 = ha_lines[1] if len(ha_lines) > 1 else ""
    ha_l3 = ha_lines[2] if len(ha_lines) > 2 else ""
    
    # Hub B OLED lines
    hb_lines = hub_b_oled.split('\n')
    hb_l1 = hb_lines[0] if len(hb_lines) > 0 else ""
    hb_l2 = hb_lines[1] if len(hb_lines) > 1 else ""
    hb_l3 = hb_lines[2] if len(hb_lines) > 2 else ""
    
    # LEDs Color strings
    ha_green_led = "\033[92mON \033[0m" if hub_a_green else "OFF"
    ha_red_led = "\033[91mON \033[0m" if hub_a_red else "OFF"
    hb_green_led = "\033[92mON \033[0m" if hub_b_green else "OFF"
    hb_red_led = "\033[91mON \033[0m" if hub_b_red else "OFF"
    
    # Buzzer
    ha_buz = f"\033[93m{hub_a_buzzer}\033[0m" if hub_a_buzzer != "OFF" else "OFF"
    hb_buz = f"\033[93m{hub_b_buzzer}\033[0m" if hub_b_buzzer != "OFF" else "OFF"
    
    print("       [ SMART HUB A: CENTRAL ]                  [ SMART HUB B: RELAY ]")
    print("========================================  ========================================")
    print(" [ OLED DISPLAY ]                         [ OLED DISPLAY ]")
    print(" +------------------------------------+   +------------------------------------+")
    print(f" | {ha_l1:<34} |   | {hb_l1:<34} |")
    print(f" | {ha_l2:<34} |   | {hb_l2:<34} |")
    print(f" | {ha_l3:<34} |   | {hb_l3:<34} |")
    print(" +------------------------------------+   +------------------------------------+")
    print(f" LEDs:   Green: [{ha_green_led}]   Red: [{ha_red_led}]        LEDs:   Green: [{hb_green_led}]   Red: [{hb_red_led}]")
    print(f" Buzzer: [{ha_buz:<14}]                  Buzzer: [{hb_buz:<14}]")
    print("========================================  ========================================")
    print(f"Last Backend Response: {last_backend_response}")
    print("--------------------------------------------------------------------------------")
    print("Controls:")
    print(" [1] Scan Tag at HUB-A                    [2] Scan Tag at HUB-B")
    print(" [T] Toggle Tamper Switch on Tag          [+] Increase Tag Temp   [-] Decrease Tag Temp")
    print(" [R] Reset Demo (Backend & Simulator)     [Q] Exit Simulation")
    print("================================================================================")

def simulate_scan_hub_a():
    global hub_a_oled, hub_a_green, hub_a_red, hub_a_buzzer, last_backend_response, last_esp_now_message
    global hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta, hub_b_oled
    
    hub_a_oled = "COMMUNICATING...\nConnecting to backend..."
    draw_interface()
    
    # Payload matching config
    payload = {
        "device_id": "ESP32-HUB-A-01",
        "hub_id": "HUB-A",
        "parcel_id": tag_parcel_id,
        "rfid_uid": "RFID4A8B9C104",
        "qr_payload": f"http://localhost:5173/scan/HUB-A?parcel_id={tag_parcel_id}",
        "temperature_c": tag_temp,
        "button_pressed": tag_tamper,
        "lat": 11.0168,
        "lng": 76.9558,
        "timestamp": "2026-06-08T15:00:00Z",
        "ble_verified": True,
        "ble_rssi_m": 1.2,
        "esp_now_prior_acceptance": False,
        "esp_now_prior_hub": "",
        "esp_now_trust_delta": 0.0
    }
    
    code, res = make_post_request(SCAN_ENDPOINT, payload)
    
    if code == 200:
        accepted = res.get("accepted", False)
        led_color = res.get("led", "red").upper()
        msg = res.get("message", "")
        decision = res.get("decision", "blocked").upper()
        
        last_backend_response = f"Code 200 - {decision}: {msg}"
        
        if accepted:
            hub_a_green = True
            hub_a_red = False
            hub_a_buzzer = "BEEP! (OK)"
            hub_a_oled = f"DECISION: ACCEPTED\nParcel: {tag_parcel_id}\nProof-of-Movement OK"
            
            # Simulate ESP-NOW transmit to HUB-B
            last_esp_now_message = f"HUB_ACCEPTED for {tag_parcel_id}"
            hub_b_cache_acceptance = True
            hub_b_cache_hub = "HUB-A"
            hub_b_cache_delta = 0.01
            hub_b_oled = f"--- HUB-B ---\nSTATUS: INCOMING\nParcel: {tag_parcel_id} from HUB-A"
            
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
            hub_a_buzzer = "BEEP BEEP BEEP!"
            hub_a_oled = f"DECISION: {decision}\nANOMALY BLOCKED!\n{msg[:30]}..."
    else:
        last_backend_response = f"Error: {res.get('error', 'Unknown Error')}"
        hub_a_green = False
        hub_a_red = True
        hub_a_buzzer = "LONG BEEP!"
        hub_a_oled = f"ERROR:\nServer Unreachable\nVerify backend is on port 8000"
        
    draw_interface()
    time.sleep(2.0)
    hub_a_green = False
    hub_a_red = False
    hub_a_buzzer = "OFF"
    hub_a_oled = "HUB-A STATUS: READY\nScan RFID Tag to verify..."
    draw_interface()

def simulate_scan_hub_b():
    global hub_b_oled, hub_b_green, hub_b_red, hub_b_buzzer, last_backend_response
    global hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta
    
    hub_b_oled = "COMMUNICATING...\nConnecting to backend..."
    draw_interface()
    
    payload = {
        "device_id": "ESP32-HUB-B-01",
        "hub_id": "HUB-B",
        "parcel_id": tag_parcel_id,
        "rfid_uid": "RFID4A8B9C104",
        "qr_payload": f"http://localhost:5173/scan/HUB-B?parcel_id={tag_parcel_id}",
        "temperature_c": tag_temp,
        "button_pressed": tag_tamper,
        "lat": 11.0250,
        "lng": 76.9650,
        "timestamp": "2026-06-08T15:00:00Z",
        "ble_verified": True,
        "ble_rssi_m": 1.2,
        "esp_now_prior_acceptance": hub_b_cache_acceptance,
        "esp_now_prior_hub": hub_b_cache_hub if hub_b_cache_acceptance else "",
        "esp_now_trust_delta": hub_b_cache_delta if hub_b_cache_acceptance else 0.0
    }
    
    # Clear cache
    hub_b_cache_acceptance = False
    hub_b_cache_hub = ""
    hub_b_cache_delta = 0.0
    
    code, res = make_post_request(SCAN_ENDPOINT, payload)
    
    if code == 200:
        accepted = res.get("accepted", False)
        led_color = res.get("led", "red").upper()
        msg = res.get("message", "")
        decision = res.get("decision", "blocked").upper()
        
        last_backend_response = f"Code 200 - {decision}: {msg}"
        
        if accepted:
            hub_b_green = True
            hub_b_red = False
            hub_b_buzzer = "BEEP! (OK)"
            hub_b_oled = f"DECISION: ACCEPTED\nParcel: {tag_parcel_id}\nProof-of-Movement OK"
        else:
            hub_b_green = False
            hub_b_red = True
            hub_b_buzzer = "BEEP BEEP BEEP!"
            hub_b_oled = f"DECISION: {decision}\nANOMALY BLOCKED!\n{msg[:30]}..."
    else:
        last_backend_response = f"Error: {res.get('error', 'Unknown Error')}"
        hub_b_green = False
        hub_b_red = True
        hub_b_buzzer = "LONG BEEP!"
        hub_b_oled = f"ERROR:\nServer Unreachable\nVerify backend is on port 8000"
        
    draw_interface()
    time.sleep(2.0)
    hub_b_green = False
    hub_b_red = False
    hub_b_buzzer = "OFF"
    hub_b_oled = "HUB-B STATUS: READY\nScan RFID Tag to verify..."
    draw_interface()

def reset_demo():
    global last_backend_response, tag_temp, tag_tamper, hub_b_cache_acceptance, hub_b_cache_hub, hub_b_cache_delta
    global hub_a_oled, hub_b_oled, last_esp_now_message
    
    code, res = make_post_request(RESET_ENDPOINT, {})
    if code == 200:
        last_backend_response = "Demo Reset Complete - Database Refreshed!"
    else:
        last_backend_response = f"Demo Reset Failed: {res.get('error', 'Unknown Error')}"
        
    tag_temp = 24.3
    tag_tamper = False
    hub_b_cache_acceptance = False
    hub_b_cache_hub = ""
    hub_b_cache_delta = 0.0
    last_esp_now_message = "No messages sent (Reset)"
    hub_a_oled = "HUB-A STATUS: READY\nScan RFID Tag to verify..."
    hub_b_oled = "HUB-B STATUS: READY\nScan RFID Tag to verify..."
    draw_interface()

def main():
    global tag_tamper, tag_temp
    
    # Configure console character encoding for Windows command prompts
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
        elif cmd == '+':
            tag_temp += 0.5
        elif cmd == '-':
            tag_temp -= 0.5
        elif cmd == 'R':
            reset_demo()
        elif cmd == 'Q':
            print("Exiting simulator.")
            break
        else:
            print("Invalid Option. Press enter to continue...")
            time.sleep(1)

if __name__ == '__main__':
    main()
