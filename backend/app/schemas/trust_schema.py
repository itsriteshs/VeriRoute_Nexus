# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: trust board and history response schemas.

from pydantic import BaseModel


class TrustHubItem(BaseModel):
    hub_id: str
    name: str
    trust_score: float
    trust_status: str
    anomaly_count: int
    routing_behavior: str
    status: str


class TrustBoardResponse(BaseModel):
    hubs: list[TrustHubItem]


class TrustHistoryItem(BaseModel):
    old_score: float
    new_score: float
    delta: float
    reason: str
    event_id: int | None
    timestamp: str


class TrustHistoryResponse(BaseModel):
    hub_id: str
    history: list[TrustHistoryItem]
