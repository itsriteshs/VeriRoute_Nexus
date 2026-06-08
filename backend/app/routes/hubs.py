# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: hubs API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Hub
from app.schemas.hub_schema import HubsResponse

router = APIRouter(prefix="/hubs", tags=["hubs"])


def trust_status(score: float) -> str:
    if score >= 0.80:
        return "trusted"
    if score >= 0.60:
        return "watch"
    if score >= 0.40:
        return "risky"
    return "quarantined"


@router.get("", response_model=HubsResponse)
def list_hubs(db: Session = Depends(get_db)):
    hubs = db.query(Hub).order_by(Hub.id).all()
    return {
        "hubs": [
            {
                "id": hub.id,
                "name": hub.name,
                "lat": hub.lat,
                "lng": hub.lng,
                "geofence_radius_m": hub.geofence_radius_m,
                "trust_score": hub.trust_score,
                "trust_status": trust_status(hub.trust_score),
                "status": hub.status,
                "congestion": hub.congestion,
                "cold_chain": hub.cold_chain,
                "anomaly_count": hub.anomaly_count,
            }
            for hub in hubs
        ]
    }
