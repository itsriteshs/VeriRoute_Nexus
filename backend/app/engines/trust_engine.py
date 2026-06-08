# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: hub trust scoring and trust history persistence.

from sqlalchemy.orm import Session

from app.core import constants
from app.db.models import Event, Hub, TrustHistory
from app.utils.time_utils import utc_now_iso


def clamp_score(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 2)


def get_trust_status(score: float) -> str:
    if score >= 0.80:
        return "trusted"
    if score >= 0.60:
        return "watch"
    if score >= 0.40:
        return "risky"
    return "quarantined"


def get_routing_behavior(score: float) -> str:
    status = get_trust_status(score)
    if status == "trusted":
        return "normal"
    if status == "watch":
        return "slight_penalty"
    if status == "risky":
        return "avoid_unless_required"
    return "excluded_from_routing"


def calculate_trust_delta(decision: str, failed_checks: list[str]) -> float:
    failed = set(failed_checks)
    if decision == constants.DECISION_ACCEPTED and not failed_checks:
        delta = 0.01
    elif decision == constants.DECISION_WARNING:
        delta = -0.04
    elif decision == constants.DECISION_REROUTED and "cold_chain" in failed:
        delta = -0.08
    elif decision == constants.DECISION_HOLD and "tamper" in failed:
        delta = -0.20
    elif decision == constants.DECISION_BLOCKED and "clone_scan" in failed:
        delta = -0.25
    elif decision == constants.DECISION_BLOCKED and "speed" in failed:
        delta = -0.20
    elif decision == constants.DECISION_BLOCKED and "route_graph" in failed:
        delta = -0.18
    elif decision == constants.DECISION_BLOCKED and failed == {"geofence"}:
        delta = -0.15
    elif decision == constants.DECISION_BLOCKED and "geofence" in failed:
        delta = -0.15
    else:
        delta = 0.0

    if len(failed_checks) > 1:
        delta -= 0.05
    return max(-0.30, min(0.02, delta))


def update_hub_trust(
    db: Session,
    hub_id: str,
    decision: str,
    failed_checks: list[str],
    reason: str,
    event_id: int | None,
    esp_now_trust_delta: float | None = None,
) -> dict[str, float | str]:
    hub = db.get(Hub, hub_id)
    if hub is None:
        raise ValueError("Hub not found")

    old_score = float(hub.trust_score)
    now = utc_now_iso()

    # Bayesian update logic
    alpha_delta = 0
    beta_delta = 0

    if decision == constants.DECISION_ACCEPTED and not failed_checks:
        alpha_delta = 1
    elif decision == constants.DECISION_HOLD or "tamper" in failed_checks:
        beta_delta = 3
    elif decision == constants.DECISION_BLOCKED:
        beta_delta = 2
    elif decision == constants.DECISION_WARNING or decision == constants.DECISION_REROUTED:
        beta_delta = 1

    if esp_now_trust_delta is not None:
        if esp_now_trust_delta > 0:
            alpha_delta += 1
        elif esp_now_trust_delta < 0:
            beta_delta += 1

    hub.alpha += alpha_delta
    hub.beta += beta_delta

    denom = hub.alpha + hub.beta
    new_score = round(float(hub.alpha) / denom, 2) if denom > 0 else 1.0
    delta = round(new_score - old_score, 2)

    hub.trust_score = new_score
    hub.updated_at = now
    
    if alpha_delta < beta_delta:
        hub.anomaly_count += 1
    if new_score < 0.40:
        hub.status = "quarantined"

    db.add(
        TrustHistory(
            hub_id=hub_id,
            old_score=old_score,
            new_score=new_score,
            delta=delta,
            reason=reason,
            event_id=event_id,
            timestamp=now,
        )
    )
    db.add(
        Event(
            event_type=constants.TRUST_UPDATED,
            parcel_id=None,
            hub_id=hub_id,
            timestamp=now,
            decision=decision,
            action=constants.TRUST_UPDATED,
            severity="info" if delta >= 0 else "warning",
            reason=reason,
        )
    )
    db.commit()
    return {"hub_id": hub_id, "old_score": old_score, "new_score": new_score, "delta": delta}
