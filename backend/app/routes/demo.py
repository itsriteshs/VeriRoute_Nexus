# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: demo API routes.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.seed_data import seed_demo_data

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/seed")
def seed_demo(db: Session = Depends(get_db)):
    return seed_demo_data(db)


@router.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    seed_demo_data(db)
    return {"status": "reset_complete", "message": "Demo state restored."}
