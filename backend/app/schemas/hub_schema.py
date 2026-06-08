# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: hub response schemas.

from pydantic import BaseModel


class HubOut(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    geofence_radius_m: float
    trust_score: float
    trust_status: str
    status: str
    congestion: float
    cold_chain: bool
    anomaly_count: int


class HubsResponse(BaseModel):
    hubs: list[HubOut]
