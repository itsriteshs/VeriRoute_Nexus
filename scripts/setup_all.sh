#!/usr/bin/env bash
set -euo pipefail
echo "VeriRoute Nexus setup"
echo "Run backend and frontend setup separately."
echo "Backend: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && ./run.sh"
echo "Frontend: cd frontend && npm install && npm run dev"
echo "This script does not assume npm or pip are installed."
