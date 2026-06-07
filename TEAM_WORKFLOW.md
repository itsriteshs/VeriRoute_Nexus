# Team Workflow

Person 1 owns `backend/`. Person 2 owns `frontend/`. Person 3 owns `hardware/` and `presentation/`.

Shared files require communication: `API_CONTRACT.md`, `DEMO_RUNBOOK.md`, `INTEGRATION_CHECKLIST.md`, and `data/demo_*.json`.

## Daily Sync Format

1. What changed yesterday?
2. What changes today?
3. Which shared contract or demo file is touched?
4. What is blocked?
5. What proof is available?

## Integration Checkpoint Rules

- Update `API_CONTRACT.md` before changing implementation shape.
- Notify the team before changing demo JSON.
- Run reset, seed, create parcel, scan, scenario, metrics, and WebSocket checks before demo practice.
- Update your progress file before commit.
