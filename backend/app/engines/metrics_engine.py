# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: derived demo metrics.

from sqlalchemy.orm import Session

from app.core import constants
from app.db.models import Event, Hub


def get_starter_metrics(db: Session | None = None) -> dict[str, object]:
    if db is None:
        return {
            "scan_validation_latency_ms": 0,
            "reroute_time_ms": 0,
            "anomalies_blocked": 0,
            "reroutes_triggered": 0,
            "cold_chain_breaches": 0,
            "fake_scans_blocked": 0,
            "trust_quarantines": 0,
            "fallback_reliability": True,
        }

    return {
        "scan_validation_latency_ms": 0,
        "reroute_time_ms": 0,
        "anomalies_blocked": db.query(Event).filter(Event.decision == constants.DECISION_BLOCKED).count(),
        "reroutes_triggered": db.query(Event)
        .filter((Event.decision == constants.DECISION_REROUTED) | (Event.event_type == constants.REROUTE_TRIGGERED))
        .count(),
        "cold_chain_breaches": db.query(Event).filter(Event.event_type == constants.TEMPERATURE_BREACH).count(),
        "fake_scans_blocked": db.query(Event).filter(Event.event_type == constants.FAKE_SCAN_BLOCKED).count(),
        "trust_quarantines": db.query(Hub)
        .filter((Hub.trust_score < 0.40) | (Hub.status == "quarantined"))
        .count(),
        "fallback_reliability": True,
    }
