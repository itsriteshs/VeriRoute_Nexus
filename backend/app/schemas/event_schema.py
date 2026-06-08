# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: event ledger response schemas.

from pydantic import BaseModel


class EventOut(BaseModel):
    id: int
    event_type: str
    parcel_id: str | None
    hub_id: str | None
    timestamp: str
    gps_lat: float | None
    gps_lng: float | None
    gps_accuracy_m: float | None
    temperature_c: float | None
    decision: str | None
    action: str | None
    severity: str | None
    reason: str | None
    raw_payload: str | None


class EventsResponse(BaseModel):
    events: list[EventOut]


class ParcelEventsResponse(BaseModel):
    parcel_id: str
    events: list[EventOut]
