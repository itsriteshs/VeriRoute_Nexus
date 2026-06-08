# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: SQLAlchemy models for the Phase 1 backend ledger and demo state.

from sqlalchemy import Boolean, Float, Integer, String, Text, event, text
from sqlalchemy.orm import Mapped, mapped_column
import hashlib

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


IS_OFFLINE = False


@event.listens_for(Event, "before_insert")
def receive_before_insert(mapper, connection, target):
    # Set synced flag based on offline simulation status
    target.synced = not IS_OFFLINE

    # Only calculate prev_hash if not already set manually and parcel_id exists
    if not target.prev_hash and target.parcel_id:
        result = connection.execute(
            text("SELECT event_hash FROM events WHERE parcel_id = :parcel_id ORDER BY id DESC LIMIT 1"),
            {"parcel_id": target.parcel_id}
        ).fetchone()
        if result and result[0]:
            target.prev_hash = result[0]
        else:
            target.prev_hash = "GENESIS"
    elif not target.prev_hash:
        target.prev_hash = "GENESIS"

    # Calculate event_hash = SHA256(event_type + parcel_id + hub_id + timestamp + raw_payload + prev_hash)
    et = target.event_type or ""
    pi = target.parcel_id or ""
    hi = target.hub_id or ""
    ts = target.timestamp or ""
    rp = target.raw_payload or ""
    ph = target.prev_hash or ""
    
    payload_str = f"{et}{pi}{hi}{ts}{rp}{ph}"
    target.event_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()


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
    zero_trust_handshake: Mapped[str | None] = mapped_column(String, nullable=True)
    mesh_consensus: Mapped[str | None] = mapped_column(String, nullable=True)
    statistical_anomaly: Mapped[str | None] = mapped_column(String, nullable=True)
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
