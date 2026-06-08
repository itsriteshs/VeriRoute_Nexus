# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: PacketFlow route request and response schemas.

from typing import Any

from pydantic import BaseModel


class RouteNextHopRequest(BaseModel):
    parcel_id: str
    current_hub: str | None = None
    destination_hub: str | None = None


class CandidateScore(BaseModel):
    hub_id: str
    full_route: list[str]
    total_eta_min: float
    sla_risk: float
    congestion_risk: float
    trust_risk: float
    condition_risk: float
    cost_emission_score: float
    final_score: float
    selected: bool = False
    rejection_reason: str | None = None


class RouteDecisionResponse(BaseModel):
    parcel_id: str
    current_hub: str
    destination_hub: str
    selected_next_hop: str | None
    full_route: list[str]
    total_eta_min: float
    final_score: float
    candidate_scores: list[CandidateScore]
    reason: str


class RouteHistoryItem(BaseModel):
    id: int
    parcel_id: str
    current_hub: str
    selected_next_hop: str | None
    full_route: list[str]
    candidate_scores: list[dict[str, Any]]
    final_score: float | None
    reason: str | None
    created_at: str
