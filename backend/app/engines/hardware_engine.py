# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Hardware helper engines for normalising scans, parsing context, and generating device actuator signals.

from typing import Any
from app.schemas.hardware_schema import HardwareScanRequest


def normalize_hardware_scan_payload(payload: HardwareScanRequest) -> dict[str, Any]:
    # qr_verified priority: If missing (None), default to True
    qr_val = True if payload.qr_verified is None else payload.qr_verified

    # Temperature priority
    temp_val = None
    if payload.temperature_c is not None:
        temp_val = payload.temperature_c
    elif payload.ble_temperature_c is not None:
        temp_val = payload.ble_temperature_c

    # Tamper priority: True if either is True
    tamper_val = payload.tamper or bool(payload.ble_tamper)

    # GPS coordinates
    gps_dict = None
    if payload.gps is not None:
        gps_dict = {
            "lat": payload.gps.lat,
            "lng": payload.gps.lng,
            "accuracy_m": payload.gps.accuracy_m,
        }

    return {
        "parcel_id": payload.parcel_id,
        "hub_id": payload.hub_id,
        "scanner_id": payload.scanner_id,
        "rfid_verified": payload.rfid_verified,
        "qr_verified": qr_val,
        "gps": gps_dict,
        "temperature_c": temp_val,
        "carrier_type": payload.carrier_type,
        "tamper": tamper_val,
        "ble_verified": payload.ble_verified,
        "ble_rssi_m": payload.ble_rssi_m,
        "esp_now_prior_acceptance": payload.esp_now_prior_acceptance,
        "esp_now_prior_hub": payload.esp_now_prior_hub,
        "esp_now_trust_delta": payload.esp_now_trust_delta,
    }


def build_hardware_context(payload: HardwareScanRequest) -> dict[str, Any]:
    context = {
        "scanner_id": payload.scanner_id,
        "rfid_verified": payload.rfid_verified,
        "ble_verified": payload.ble_verified if payload.ble_verified is not None else False,
        "ble_identity_mismatch": False,
        "esp_now_prior_acceptance": payload.esp_now_prior_acceptance
        if payload.esp_now_prior_acceptance is not None
        else False,
    }

    if payload.ble_parcel_id and payload.ble_parcel_id != payload.parcel_id:
        context["ble_identity_mismatch"] = True
    if payload.ble_rssi_m is not None:
        context["ble_rssi_m"] = payload.ble_rssi_m
    if payload.esp_now_prior_hub:
        context["esp_now_prior_hub"] = payload.esp_now_prior_hub
    if payload.esp_now_trust_delta is not None:
        context["esp_now_trust_delta"] = payload.esp_now_trust_delta
    if payload.esp_now_message_type:
        context["esp_now_message_type"] = payload.esp_now_message_type

    return context


def generate_hardware_command(
    hub_id: str,
    parcel_id: str,
    decision: str,
    led: str,
    reason: str,
    failed_checks: list[str] = None,
) -> dict[str, Any]:
    failed = failed_checks or []
    oled_text = "STATUS: UNKNOWN"
    buzzer = False

    if decision == "ACCEPTED":
        oled_text = "ACCEPTED"
        buzzer = False
    elif decision == "REROUTED":
        oled_text = "REROUTED: TEMP"
        buzzer = True
    elif decision == "HOLD":
        oled_text = "HOLD: TAMPER"
        buzzer = True
    elif decision == "BLOCKED":
        buzzer = True
        if "geofence" in failed:
            oled_text = "BLOCKED: GEOFENCE"
        elif "clone_scan" in failed:
            oled_text = "BLOCKED: CLONE"
        elif "speed" in failed:
            oled_text = "BLOCKED: SPEED"
        elif "route_graph" in failed:
            oled_text = "BLOCKED: ROUTE"
        else:
            oled_text = "BLOCKED: ANOMALY"
    elif decision == "WARNING":
        oled_text = "WARNING: REVIEW"
        buzzer = False

    return {
        "hub_id": hub_id,
        "parcel_id": parcel_id,
        "decision": decision,
        "led": led,
        "oled_text": oled_text,
        "buzzer": buzzer,
    }
