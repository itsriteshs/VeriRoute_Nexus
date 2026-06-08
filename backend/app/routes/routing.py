# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: PacketFlow routing API routes.

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Parcel, RouteDecision
from app.engines.routing_engine import select_next_hop
from app.schemas.route_schema import (
    RouteDecisionResponse,
    RouteHistoryItem,
    RouteNextHopRequest,
)

router = APIRouter(prefix="/route", tags=["route"])


def _http_error(error: ValueError) -> HTTPException:
    message = str(error)
    if message in {"Parcel not found"}:
        return HTTPException(status_code=404, detail="Parcel not found")
    if message in {"Current hub not found", "Destination hub not found", "Hub not found"}:
        return HTTPException(status_code=404, detail="Hub not found")
    return HTTPException(status_code=400, detail=message)


def _parse_json_field(value: str | None, fallback: Any) -> Any:
    if not value:
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def serialize_route_decision(decision: RouteDecision) -> dict[str, object]:
    return {
        "id": decision.id,
        "parcel_id": decision.parcel_id,
        "current_hub": decision.current_hub,
        "selected_next_hop": decision.selected_next_hop,
        "full_route": _parse_json_field(decision.full_route, []),
        "candidate_scores": _parse_json_field(decision.candidate_scores, []),
        "final_score": decision.final_score,
        "reason": decision.reason,
        "created_at": decision.created_at or "",
    }


@router.post("/next-hop", response_model=RouteDecisionResponse)
async def next_hop(payload: RouteNextHopRequest, db: Session = Depends(get_db)):
    try:
        result = select_next_hop(db, payload.parcel_id, payload.current_hub, payload.destination_hub)
        await safe_broadcast("route_decision", {
            "parcel_id": result["parcel_id"],
            "current_hub": result["current_hub"],
            "selected_next_hop": result["selected_next_hop"],
            "full_route": result["full_route"],
            "candidate_scores": result["candidate_scores"],
            "reason": result["reason"]
        })
        return result
    except ValueError as error:
        raise _http_error(error) from error


@router.get("/decisions", response_model=list[RouteHistoryItem])
def route_decisions(db: Session = Depends(get_db)):
    decisions = db.query(RouteDecision).order_by(RouteDecision.id.desc()).limit(50).all()
    return [serialize_route_decision(decision) for decision in decisions]


@router.get("/decisions/{parcel_id}", response_model=list[RouteHistoryItem])
def parcel_route_decisions(parcel_id: str, db: Session = Depends(get_db)):
    decisions = (
        db.query(RouteDecision)
        .filter(RouteDecision.parcel_id == parcel_id)
        .order_by(RouteDecision.id.desc())
        .all()
    )
    return [serialize_route_decision(decision) for decision in decisions]


@router.get("/{parcel_id}")
def latest_route(parcel_id: str, db: Session = Depends(get_db)):
    parcel = db.get(Parcel, parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")

    decision = (
        db.query(RouteDecision)
        .filter(RouteDecision.parcel_id == parcel_id)
        .order_by(RouteDecision.id.desc())
        .first()
    )
    if decision is None:
        try:
            result = select_next_hop(db, parcel_id, parcel.current_hub, parcel.destination_hub)
        except ValueError as error:
            raise _http_error(error) from error
        return {
            "parcel_id": parcel_id,
            "current_route": result["full_route"],
            "selected_next_hop": result["selected_next_hop"],
            "latest_reason": result["reason"],
        }

    return {
        "parcel_id": parcel_id,
        "current_route": _parse_json_field(decision.full_route, []),
        "selected_next_hop": decision.selected_next_hop,
        "latest_reason": decision.reason,
    }
