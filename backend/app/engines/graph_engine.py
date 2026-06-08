# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: usable route graph helpers for PacketFlow.

from heapq import heappop, heappush

from sqlalchemy.orm import Session

from app.db.models import Edge, Hub

HIGH_ETA = 1_000_000.0


def get_trust_status(trust_score: float) -> str:
    if trust_score >= 0.80:
        return "trusted"
    if trust_score >= 0.60:
        return "watch"
    if trust_score >= 0.40:
        return "risky"
    return "quarantined"


def is_usable_hub(hub: Hub | None) -> bool:
    return hub is not None and hub.status != "failed" and hub.trust_score >= 0.40


def get_neighbors(db: Session, hub_id: str) -> list[Hub]:
    if not is_usable_hub(db.get(Hub, hub_id)):
        return []

    edges = (
        db.query(Edge)
        .filter(Edge.from_hub == hub_id, Edge.status == "active")
        .order_by(Edge.eta_min, Edge.to_hub)
        .all()
    )
    neighbors = []
    for edge in edges:
        hub = db.get(Hub, edge.to_hub)
        if is_usable_hub(hub):
            neighbors.append(hub)
    return neighbors


def get_active_edge(db: Session, from_hub: str, to_hub: str) -> Edge | None:
    return (
        db.query(Edge)
        .filter(
            Edge.from_hub == from_hub,
            Edge.to_hub == to_hub,
            Edge.status == "active",
        )
        .first()
    )


def get_effective_eta(edge: Edge) -> float:
    traffic_risk = float(edge.traffic_risk or 0.0)
    weather_risk = float(edge.weather_risk or 0.0)
    eff_traffic = traffic_risk if traffic_risk > 0.30 else 0.0
    eff_weather = weather_risk if weather_risk > 0.30 else 0.0
    return float(edge.eta_min) * (1.0 + eff_traffic * 0.75 + eff_weather * 0.50)


def find_shortest_route_by_eta(db: Session, start_hub: str, destination_hub: str) -> tuple[list[str], float]:
    if not is_usable_hub(db.get(Hub, start_hub)) or not is_usable_hub(db.get(Hub, destination_hub)):
        return [], HIGH_ETA

    queue: list[tuple[float, str, list[str]]] = [(0.0, start_hub, [start_hub])]
    best_eta: dict[str, float] = {start_hub: 0.0}

    while queue:
        eta_so_far, hub_id, path = heappop(queue)
        if hub_id == destination_hub:
            return path, eta_so_far
        if eta_so_far > best_eta.get(hub_id, HIGH_ETA):
            continue

        for neighbor in get_neighbors(db, hub_id):
            edge = get_active_edge(db, hub_id, neighbor.id)
            if edge is None:
                continue
            next_eta = eta_so_far + get_effective_eta(edge)
            if next_eta < best_eta.get(neighbor.id, HIGH_ETA):
                best_eta[neighbor.id] = next_eta
                heappush(queue, (next_eta, neighbor.id, [*path, neighbor.id]))

    return [], HIGH_ETA


def find_route_via_candidate(
    db: Session,
    current_hub: str,
    candidate_hub: str,
    destination_hub: str,
) -> tuple[list[str], float]:
    first_edge = get_active_edge(db, current_hub, candidate_hub)
    if first_edge is None or not is_usable_hub(db.get(Hub, candidate_hub)):
        return [], HIGH_ETA

    tail_route, tail_eta = find_shortest_route_by_eta(db, candidate_hub, destination_hub)
    if not tail_route:
        return [], HIGH_ETA

    return [current_hub, *tail_route], get_effective_eta(first_edge) + tail_eta
