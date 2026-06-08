# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: starter metrics response schema.

from pydantic import BaseModel


class MetricsResponse(BaseModel):
    scan_validation_latency_ms: int
    reroute_time_ms: int
    anomalies_blocked: int
    reroutes_triggered: int
    cold_chain_breaches: int
    fake_scans_blocked: int
    trust_quarantines: int
    fallback_reliability: bool
