# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: trust board API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Hub, TrustHistory
from app.engines.trust_engine import get_routing_behavior, get_trust_status
from app.schemas.trust_schema import TrustBoardResponse, TrustHistoryResponse

router = APIRouter(prefix="/trust", tags=["trust"])


@router.get("/hubs", response_model=TrustBoardResponse)
def trust_hubs(db: Session = Depends(get_db)):
    hubs = db.query(Hub).order_by(Hub.id).all()
    return {
        "hubs": [
            {
                "hub_id": hub.id,
                "name": hub.name,
                "trust_score": hub.trust_score,
                "trust_status": get_trust_status(hub.trust_score),
                "anomaly_count": hub.anomaly_count,
                "routing_behavior": get_routing_behavior(hub.trust_score),
                "status": hub.status,
            }
            for hub in hubs
        ]
    }


@router.get("/history/{hub_id}", response_model=TrustHistoryResponse)
def trust_history(hub_id: str, db: Session = Depends(get_db)):
    history = (
        db.query(TrustHistory)
        .filter(TrustHistory.hub_id == hub_id)
        .order_by(TrustHistory.id.desc())
        .all()
    )
    return {
        "hub_id": hub_id,
        "history": [
            {
                "old_score": row.old_score,
                "new_score": row.new_score,
                "delta": row.delta,
                "reason": row.reason,
                "event_id": row.event_id,
                "timestamp": row.timestamp,
            }
            for row in history
        ],
    }
