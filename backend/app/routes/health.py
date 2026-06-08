from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.db.models import Hub, Edge, Parcel
from app.engines.routing_engine import select_next_hop
from app.core.websocket_manager import websocket_manager
from app.utils.time_utils import utc_now_iso

router = APIRouter()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    db_status = "connected"
    seed_state = "missing"
    try:
        db.execute(text("SELECT 1"))
        hubs_count = db.query(Hub).count()
        parcel_exists = db.get(Parcel, "MED-104") is not None
        if hubs_count >= 7 and parcel_exists:
            seed_state = "ready"
    except Exception:
        db_status = "error"
        seed_state = "missing"

    return {
        "status": "ok",
        "service": "PacketFlow ImmuneNet Backend",
        "version": "1.0",
        "database": db_status,
        "websocket": "available",
        "seed_state": seed_state,
        "timestamp": utc_now_iso(),
    }


@router.get("/ready")
def ready(db: Session = Depends(get_db)):
    checks = {
        "database": False,
        "hubs_seeded": False,
        "edges_seeded": False,
        "demo_parcel_seeded": False,
        "routing_available": False,
        "websocket_available": False
    }

    try:
        db.execute(text("SELECT 1"))
        checks["database"] = True
    except Exception:
        pass

    try:
        hubs_count = db.query(Hub).count()
        if hubs_count >= 7:
            checks["hubs_seeded"] = True
    except Exception:
        pass

    try:
        edges_count = db.query(Edge).count()
        if edges_count >= 8:
            checks["edges_seeded"] = True
    except Exception:
        pass

    try:
        parcel = db.get(Parcel, "MED-104")
        if parcel is not None:
            checks["demo_parcel_seeded"] = True
    except Exception:
        pass

    if checks["database"] and checks["hubs_seeded"] and checks["edges_seeded"] and checks["demo_parcel_seeded"]:
        try:
            result = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")
            if result is not None and result.get("selected_next_hop") is not None:
                checks["routing_available"] = True
        except Exception:
            pass

    if websocket_manager is not None:
        checks["websocket_available"] = True

    is_ready = all(checks.values())
    message = "PacketFlow backend is demo-ready." if is_ready else "PacketFlow backend is not fully ready."

    return {
        "ready": is_ready,
        "checks": checks,
        "message": message
    }

