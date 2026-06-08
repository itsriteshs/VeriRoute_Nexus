# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: deterministic route explanation text.

from app.db.models import Parcel


def generate_route_reason(
    parcel: Parcel,
    selected_candidate: dict[str, object] | None,
    candidate_scores: list[dict[str, object]],
) -> str:
    if selected_candidate is None:
        return "No valid route available from current hub to destination."

    next_hop = str(selected_candidate["hub_id"])
    route = selected_candidate.get("full_route") or []
    eta = float(selected_candidate.get("total_eta_min") or 0)
    trust_risk = float(selected_candidate.get("trust_risk") or 1)

    route_quality = "an SLA-safe route" if parcel.sla_minutes and eta <= parcel.sla_minutes else "the best available route"
    strengths = []
    if parcel.sla_minutes and eta <= parcel.sla_minutes:
        route_quality = "an SLA-safe route"
    else:
        route_quality = "the best available route"

    if trust_risk <= 0.20:
        strengths.append("high hub trust")

    cold_sensitive = parcel.parcel_type in {"medicine", "vaccine", "food", "dairy", "seafood", "cold_chain"}
    if cold_sensitive and any("COLD" in hub_id or hub_id == "HUB-E" for hub_id in route[1:]):
        strengths.append("cold-chain-safe continuation")

    selected_congestion = float(selected_candidate.get("congestion_risk") or 0)
    if any(float(candidate.get("congestion_risk") or 0) - selected_congestion >= 0.25 for candidate in candidate_scores):
        strengths.append("lower congestion than a risky alternative")

    if not strengths:
        return f"{next_hop} selected because it gives {parcel.id} {route_quality}."

    if len(strengths) == 1:
        strengths_text = strengths[0]
    elif len(strengths) == 2:
        strengths_text = f"{strengths[0]} and {strengths[1]}"
    else:
        strengths_text = ", ".join(strengths[:-1]) + f", and {strengths[-1]}"
    return f"{next_hop} selected because it gives {parcel.id} {route_quality} while maintaining {strengths_text}."


def generate_scan_reason(parcel, hub, decision: str, failed_checks: list[str], check_results: dict) -> str:
    if decision == "ACCEPTED":
        return "Movement accepted because identity, GPS geofence, route validity, speed plausibility, temperature, and tamper checks passed."
    if decision == "BLOCKED" and "geofence" in failed_checks:
        return f"Scan blocked because scanner GPS was outside {hub.id} geofence."
    if decision == "BLOCKED" and "clone_scan" in failed_checks:
        return f"Clone scan blocked because {parcel.id} appeared at two hubs within an impossible time window."
    if decision == "BLOCKED" and "speed" in failed_checks:
        return check_results.get("speed", {}).get("reason") or "Scan blocked because the movement speed was impossible."
    if decision == "BLOCKED" and "route_graph" in failed_checks:
        return check_results.get("route_graph", {}).get("reason") or "Scan blocked because the hub is not a valid next hop."
    if decision == "REROUTED" and "cold_chain" in failed_checks:
        limit = parcel.temperature_limit
        return f"Cold-chain risk detected. {parcel.id} exceeded {limit:g}C, so PacketFlow recalculated a safer route through cold-chain-capable hubs."
    if decision == "HOLD" and "tamper" in failed_checks:
        return f"Tamper event detected at {hub.id}. Parcel movement has been held for review."
    if decision == "WARNING":
        return "Movement warning because one or more ImmuneNet checks could not fully verify the scan."
    return "Scan processed by ImmuneNet."
