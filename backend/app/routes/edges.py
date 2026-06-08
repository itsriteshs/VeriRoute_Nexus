# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: edges API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Edge
from app.schemas.edge_schema import EdgesResponse

router = APIRouter(prefix="/edges", tags=["edges"])


@router.get("", response_model=EdgesResponse)
def list_edges(db: Session = Depends(get_db)):
    edges = db.query(Edge).order_by(Edge.id).all()
    return {
        "edges": [
            {
                "from_hub": edge.from_hub,
                "to_hub": edge.to_hub,
                "distance_km": edge.distance_km,
                "eta_min": edge.eta_min,
                "traffic_risk": edge.traffic_risk,
                "weather_risk": edge.weather_risk,
                "status": edge.status,
            }
            for edge in edges
        ]
    }
