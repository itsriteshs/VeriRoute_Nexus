from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import constants
from app.core.websocket_manager import safe_broadcast
from app.db.database import get_db
from app.db.models import Hub, Parcel, Event
from app.engines.demo_engine import reset_demo_state, get_demo_snapshot, validate_demo_flow
from app.engines.metrics_engine import get_starter_metrics
from app.engines.routing_engine import select_next_hop
from app.routes.scan import process_and_broadcast_scan
from app.schemas.scan_schema import ScanRequest

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/seed")
async def seed_demo(db: Session = Depends(get_db)):
    res = reset_demo_state(db)
    await safe_broadcast(
        "demo_reset", {"status": "reset_complete", "message": "Demo state restored."}
    )
    await safe_broadcast("metrics_updated", get_starter_metrics(db))
    return res


@router.post("/reset")
async def reset_demo(db: Session = Depends(get_db)):
    res = reset_demo_state(db)
    await safe_broadcast(
        "demo_reset", {"status": "reset_complete", "message": "Demo state restored."}
    )
    await safe_broadcast("metrics_updated", get_starter_metrics(db))
    return res


@router.get("/snapshot")
def snapshot(db: Session = Depends(get_db)):
    return get_demo_snapshot(db)


@router.post("/validate")
async def validate(db: Session = Depends(get_db)):
    res = await validate_demo_flow(db)
    await safe_broadcast(
        "demo_reset", {"status": "reset_complete", "message": "Demo state restored."}
    )
    await safe_broadcast("metrics_updated", get_starter_metrics(db))
    return res


@router.post("/run/main-wow")
async def run_main_wow(db: Session = Depends(get_db)):
    # 1. Reset demo
    reset_res = reset_demo_state(db)
    await safe_broadcast("demo_reset", {"status": "reset_complete", "message": "Demo state restored."})
    await safe_broadcast("metrics_updated", get_starter_metrics(db))

    # 2. Calculate initial route
    init_route_res = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")

    # 3. Valid scan at HUB-A
    scan_req = ScanRequest(
        parcel_id="MED-104",
        hub_id="HUB-A",
        scanner_id="SCANNER-07",
        gps={"lat": 11.0168, "lng": 76.9558, "accuracy_m": 18},
        temperature_c=24.3,
        carrier_type="van",
        tamper=False,
    )
    valid_scan_res = await process_and_broadcast_scan(db, scan_req)

    # 4. Overload HUB-B
    hub_b = db.get(Hub, "HUB-B")
    if hub_b:
        hub_b.status = "overloaded"
        hub_b.congestion = 0.90
        db.commit()
    overload_res = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")

    # 5. Fake scan at HUB-C
    fake_scan_req = ScanRequest(
        parcel_id="MED-104",
        hub_id="HUB-C",
        scanner_id="FAKE-SCANNER",
        rfid_verified=True,
        qr_verified=True,
        gps={"lat": 11.1000, "lng": 77.1000, "accuracy_m": 20},
        temperature_c=24.3,
        carrier_type="van",
        tamper=False,
    )
    fake_scan_res = await process_and_broadcast_scan(db, fake_scan_req)

    # 6. Temperature breach
    parcel = db.get(Parcel, "MED-104")
    if parcel:
        parcel.current_temperature = 29.2
        parcel.status = "rerouted"
        parcel.current_hub = "HUB-A"
        db.commit()
    temp_breach_res = select_next_hop(db, "MED-104", "HUB-A", "CUSTOMER-ZONE")

    return {
        "status": "completed",
        "steps": [
            {"step": "reset", "result": reset_res},
            {"step": "initial_route", "result": init_route_res},
            {"step": "valid_scan", "result": valid_scan_res},
            {"step": "overload_hub", "result": overload_res},
            {"step": "fake_scan", "result": fake_scan_res},
            {"step": "temperature_breach", "result": temp_breach_res},
        ]
    }


@router.post("/toggle-sync")
async def toggle_sync(db: Session = Depends(get_db)):
    from app.db import models
    models.IS_OFFLINE = not models.IS_OFFLINE
    await safe_broadcast("sync_status_changed", {"is_offline": models.IS_OFFLINE})
    return {"status": "success", "is_offline": models.IS_OFFLINE}


@router.post("/flush-sync")
async def flush_sync(db: Session = Depends(get_db)):
    unsynced = db.query(Event).filter(Event.synced == False).all()
    for e in unsynced:
        e.synced = True
    db.commit()
    await safe_broadcast("sync_flushed", {"flushed_count": len(unsynced)})
    await safe_broadcast("metrics_updated", get_starter_metrics(db))
    return {"status": "success", "flushed_count": len(unsynced)}


