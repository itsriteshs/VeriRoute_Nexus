# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: SQLAlchemy models for the Phase 1 backend ledger and demo state.

from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Hub(Base):
    __tablename__ = "hubs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)
    geofence_radius_m: Mapped[float] = mapped_column(Float, default=75)
    trust_score: Mapped[float] = mapped_column(Float, default=1.0)
    status: Mapped[str] = mapped_column(String, default="active")
    congestion: Mapped[float] = mapped_column(Float, default=0.2)
    cold_chain: Mapped[bool] = mapped_column(Boolean, default=False)
    queue_load: Mapped[float] = mapped_column(Float, default=0.0)
    anomaly_count: Mapped[int] = mapped_column(Integer, default=0)
    alpha: Mapped[int] = mapped_column(Integer, default=10)
    beta: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String, nullable=True)


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_hub: Mapped[str] = mapped_column(String, nullable=False)
    to_hub: Mapped[str] = mapped_column(String, nullable=False)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    eta_min: Mapped[float] = mapped_column(Float, nullable=False)
    traffic_risk: Mapped[float] = mapped_column(Float, default=0.2)
    weather_risk: Mapped[float] = mapped_column(Float, default=0.0)
    cost_score: Mapped[float] = mapped_column(Float, default=0.3)
    emission_score: Mapped[float] = mapped_column(Float, default=0.3)
    allowed_carriers: Mapped[str] = mapped_column(String, default="van,bike,drone,bot")
    status: Mapped[str] = mapped_column(String, default="active")


class Parcel(Base):
    __tablename__ = "parcels"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    parcel_type: Mapped[str] = mapped_column(String, nullable=False)
    source_hub: Mapped[str] = mapped_column(String, nullable=False)
    destination_hub: Mapped[str] = mapped_column(String, nullable=False)
    current_hub: Mapped[str] = mapped_column(String, nullable=False)
    previous_hub: Mapped[str | None] = mapped_column(String, nullable=True)
    priority: Mapped[str] = mapped_column(String, default="normal")
    sla_minutes: Mapped[int] = mapped_column(Integer, default=60)
    temperature_limit: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    carrier_type: Mapped[str] = mapped_column(String, default="van")
    status: Mapped[str] = mapped_column(String, default="created")
    trust_state: Mapped[str] = mapped_column(String, default="unverified")
    created_at: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_at: Mapped[str | None] = mapped_column(String, nullable=True)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    parcel_id: Mapped[str | None] = mapped_column(String, nullable=True)
    hub_id: Mapped[str | None] = mapped_column(String, nullable=True)
    timestamp: Mapped[str] = mapped_column(String, nullable=False)
    gps_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    gps_accuracy_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    decision: Mapped[str | None] = mapped_column(String, nullable=True)
    action: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    prev_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    event_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    synced: Mapped[bool] = mapped_column(Boolean, default=True)


class ImmuneCheck(Base):
    __tablename__ = "immune_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parcel_id: Mapped[str | None] = mapped_column(String, nullable=True)
    hub_id: Mapped[str | None] = mapped_column(String, nullable=True)
    geofence: Mapped[str | None] = mapped_column(String, nullable=True)
    speed: Mapped[str | None] = mapped_column(String, nullable=True)
    route_graph: Mapped[str | None] = mapped_column(String, nullable=True)
    clone_scan: Mapped[str | None] = mapped_column(String, nullable=True)
    cold_chain: Mapped[str | None] = mapped_column(String, nullable=True)
    tamper: Mapped[str | None] = mapped_column(String, nullable=True)
    failed_checks: Mapped[str | None] = mapped_column(Text, nullable=True)
    decision: Mapped[str | None] = mapped_column(String, nullable=True)
    severity: Mapped[str | None] = mapped_column(String, nullable=True)
    action: Mapped[str | None] = mapped_column(String, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class RouteDecision(Base):
    __tablename__ = "route_decisions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parcel_id: Mapped[str] = mapped_column(String, nullable=False)
    current_hub: Mapped[str] = mapped_column(String, nullable=False)
    selected_next_hop: Mapped[str | None] = mapped_column(String, nullable=True)
    full_route: Mapped[str | None] = mapped_column(Text, nullable=True)
    candidate_scores: Mapped[str | None] = mapped_column(Text, nullable=True)
    final_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str | None] = mapped_column(String, nullable=True)


class TrustHistory(Base):
    __tablename__ = "trust_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hub_id: Mapped[str] = mapped_column(String, nullable=False)
    old_score: Mapped[float] = mapped_column(Float, nullable=False)
    new_score: Mapped[float] = mapped_column(Float, nullable=False)
    delta: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    event_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[str] = mapped_column(String, nullable=False)


class Disruption(Base):
    __tablename__ = "disruptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    disruption_type: Mapped[str] = mapped_column(String, nullable=False)
    target_id: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String, nullable=False)
    resolved_at: Mapped[str | None] = mapped_column(String, nullable=True)
