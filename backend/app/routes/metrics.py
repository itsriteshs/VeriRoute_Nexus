# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: metrics API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.engines.metrics_engine import get_starter_metrics
from app.schemas.metrics_schema import MetricsResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsResponse)
def metrics(db: Session = Depends(get_db)):
    return get_starter_metrics(db)
