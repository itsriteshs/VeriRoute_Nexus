# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: scenario request and response Pydantic models.

from pydantic import BaseModel, Field


class FailHubRequest(BaseModel):
    hub_id: str = Field(default="HUB-B")
    parcel_id: str = Field(default="MED-104")


class OverloadHubRequest(BaseModel):
    hub_id: str = Field(default="HUB-B")
    parcel_id: str = Field(default="MED-104")
    congestion: float = Field(default=0.95)


class TrafficJamRequest(BaseModel):
    from_hub: str = Field(default="HUB-B")
    to_hub: str = Field(default="HUB-E")
    parcel_id: str = Field(default="MED-104")
    traffic_risk: float = Field(default=0.95)


class WeatherRiskRequest(BaseModel):
    from_hub: str = Field(default="HUB-B")
    to_hub: str = Field(default="HUB-E")
    parcel_id: str = Field(default="MED-104")
    weather_risk: float = Field(default=0.90)


class TempBreachRequest(BaseModel):
    parcel_id: str = Field(default="MED-104")
    hub_id: str = Field(default="HUB-B")
    temperature_c: float = Field(default=29.2)


class ScenarioResponse(BaseModel):
    disruption: dict
    agentops: dict
    old_route: list[str]
    new_route: list[str]
    reason: str
