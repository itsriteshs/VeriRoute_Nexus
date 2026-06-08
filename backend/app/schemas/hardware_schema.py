# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Pydantic request and response schemas for Phase 7 + Phase 8 hardware scan and dual-node ESP-NOW relay handshakes.

from typing import Any, Optional
from pydantic import AliasChoices, BaseModel, Field, model_validator


class HardwareGPSPayload(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None
    accuracy_m: Optional[float] = None


class HardwareScanRequest(BaseModel):
    parcel_id: str
    hub_id: str
    scanner_id: str = Field(validation_alias=AliasChoices("scanner_id", "device_id"))
    rfid_verified: bool = True
    qr_verified: Optional[bool] = None
    temperature_c: Optional[float] = None
    tamper: bool = Field(default=False, validation_alias=AliasChoices("tamper", "button_pressed"))
    gps: Optional[HardwareGPSPayload] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    timestamp: Optional[str] = None
    carrier_type: Optional[str] = None

    # BLE optional fields
    ble_verified: Optional[bool] = None
    ble_parcel_id: Optional[str] = None
    ble_temperature_c: Optional[float] = None
    ble_tamper: Optional[bool] = None
    ble_rssi_m: Optional[float] = None

    # ESP-NOW optional fields
    esp_now_prior_acceptance: Optional[bool] = None
    esp_now_prior_hub: Optional[str] = None
    esp_now_trust_delta: Optional[float] = None
    esp_now_message_type: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def accept_device_native_payload(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        next_data = dict(data)
        if next_data.get("gps") is None and (
            next_data.get("lat") is not None or next_data.get("lng") is not None
        ):
            next_data["gps"] = {
                "lat": next_data.get("lat"),
                "lng": next_data.get("lng"),
            }

        if next_data.get("qr_verified") is None and next_data.get("qr_payload"):
            next_data["qr_verified"] = True

        return next_data


class HardwareScanResponse(BaseModel):
    status: str
    accepted: Optional[bool] = None
    decision: Optional[str] = None
    action: Optional[str] = None
    led: Optional[str] = None
    parcel_id: str
    hub_id: str
    requires_gps: bool = False
    gps_scan_url: Optional[str] = None
    immune_checks: Optional[dict[str, Any]] = None
    failed_checks: list[str] = []
    trust_update: Optional[dict[str, Any]] = None
    route_decision: Optional[dict[str, Any]] = None
    hardware_context: dict[str, Any]
    reason: str
    message: Optional[str] = None


class P2PHandshakeRequest(BaseModel):
    sender_hub: str
    receiver_hub: str
    parcel_id: str
    message_type: str
    trust_delta: Optional[float] = None
    failed_check: Optional[str] = None
    eta_sec: Optional[int] = None
    carrier_type: Optional[str] = None
    timestamp: Optional[str] = None


class P2PHandshakeResponse(BaseModel):
    status: str
    event_id: int
    sender_hub: str
    receiver_hub: str
    parcel_id: str
    message_type: str
    reason: str


class HardwareDecisionCommand(BaseModel):
    hub_id: str
    parcel_id: str
    decision: str
    led: str
    oled_text: str
    buzzer: bool = False
