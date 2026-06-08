# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: FastAPI application entrypoint and router registration.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.routes import demo, edges, health, hubs, ledger, metrics, parcels, routing, scan, trust

app = FastAPI(title="PacketFlow ImmuneNet Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    init_db()


app.include_router(health.router)
app.include_router(demo.router)
app.include_router(hubs.router)
app.include_router(edges.router)
app.include_router(parcels.router)
app.include_router(ledger.router)
app.include_router(metrics.router)
app.include_router(routing.router)
app.include_router(scan.router)
app.include_router(trust.router)


@app.get("/")
def root():
    return {"project": "VeriRoute Nexus", "team": "Aristotle", "message": "Proof-powered routing for trusted logistics"}
