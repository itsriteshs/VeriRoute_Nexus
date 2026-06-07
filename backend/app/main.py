# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: FastAPI application entrypoint and router registration.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health

app = FastAPI(title="VeriRoute Nexus API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.get("/")
def root():
    return {"project": "VeriRoute Nexus", "team": "Aristotle", "message": "Proof-powered routing for trusted logistics"}
