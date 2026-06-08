# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: scan validation request and response schemas.

from typing import Any

from pydantic import BaseModel


class GPSPayload(BaseModel):
    lat: float
    lng: float
    accuracy_m: float | None = None


class ScanRequest(BaseModel):
    parcel_id: str
    hub_id: str
    scanner_id: str = "MANUAL-SCANNER"
    rfid_verified: bool = True
    qr_verified: bool = True
    gps: GPSPayload | None = None
    temperature_c: float | None = None
    carrier_type: str | None = None
    previous_hub: str | None = None
    claimed_next_hub: str | None = None
    tamper: bool = False
    ble_verified: bool | None = None
    ble_rssi_m: float | None = None
    esp_now_prior_acceptance: bool | None = None
    esp_now_prior_hub: str | None = None
    esp_now_trust_delta: float | None = None
    totp_token: str | None = None
    witness_node_ids: list[str] | None = None


class FakeScanRequest(BaseModel):
    parcel_id: str = "MED-104"
    claimed_hub: str = "HUB-C"
    fake_gps: GPSPayload


class CloneScanRequest(BaseModel):
    parcel_id: str = "MED-104"
    first_hub: str = "HUB-B"
    second_hub: str = "HUB-D"


class TamperScanRequest(BaseModel):
    parcel_id: str = "MED-104"
    hub_id: str = "HUB-C"
    tamper: bool = True


class ImmuneChecksResponse(BaseModel):
    geofence: str
    speed: str
    route_graph: str
    clone_scan: str
    cold_chain: str
    tamper: str
    zero_trust_handshake: str = "PASS"
    mesh_consensus: str = "PASS"
    statistical_anomaly: str = "PASS"


class TrustUpdateResponse(BaseModel):
    hub_id: str
    old_score: float
    new_score: float
    delta: float


class ScanResponse(BaseModel):
    decision: str
    action: str
    led: str
    parcel_id: str
    hub_id: str
    immune_checks: ImmuneChecksResponse
    failed_checks: list[str]
    trust_update: TrustUpdateResponse | None
    route_decision: dict[str, Any] | None
    reason: str
