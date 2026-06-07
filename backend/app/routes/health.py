# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: Health route for smoke tests and frontend readiness checks.

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "veriroute-nexus-backend"}
