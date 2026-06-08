# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: parcel response schemas.

from pydantic import BaseModel

from app.schemas.event_schema import EventOut


class ParcelOut(BaseModel):
    id: str
    parcel_type: str
    source_hub: str
    destination_hub: str
    current_hub: str
    previous_hub: str | None
    priority: str
    sla_minutes: int
    temperature_limit: float | None
    current_temperature: float | None
    carrier_type: str
    status: str
    trust_state: str


class ParcelsResponse(BaseModel):
    parcels: list[ParcelOut]


class ParcelDetailResponse(BaseModel):
    parcel: ParcelOut
    latest_events: list[EventOut]
