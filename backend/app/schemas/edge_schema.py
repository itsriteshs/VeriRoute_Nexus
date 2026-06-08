# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: edge response schemas.

from pydantic import BaseModel


class EdgeOut(BaseModel):
    from_hub: str
    to_hub: str
    distance_km: float
    eta_min: float
    traffic_risk: float
    weather_risk: float
    status: str


class EdgesResponse(BaseModel):
    edges: list[EdgeOut]
