# Verification Log

Audit date: 2026-06-14  
This log records commands run during the judge-readiness pass. It should be refreshed immediately before final submission.

| Command | Result | Error output summary | Fix attempted | Remaining issue |
| --- | --- | --- | --- | --- |
| `python3 -m compileall -q backend` | Pass | No output. | None required. | None. |
| `cd backend && source .venv/bin/activate && pytest -q` | Pass | `33 passed, 1 warning in 1.76s`; warning is Starlette/httpx deprecation from `fastapi.testclient`. | None required. | Dependency warning is not submission-blocking. |
| `cd frontend && npm run typecheck` | Pass | `tsc --noEmit` completed with no output errors. | None required. | None. |
| `cd frontend && npm run build` | Pass | Vite built `dist/` successfully; output bundle around 274.59 kB JS and 48.93 kB CSS. | None required. | None. |
| `git diff --check` | Pass | No whitespace errors. | None required. | None. |
| Start backend on `127.0.0.1:8000` | Fail/environment conflict | Port 8000 already served a different app returning `Cannot GET /health`; uvicorn could not bind due to address in use. | Started PacketFlow backend on `127.0.0.1:8001` for smoke checks. | For normal judge flow, free port 8000 or update frontend env to point at 8001. |
| Backend health check on `127.0.0.1:8001` | Pass | `/health` returned `status: ok`, service `PacketFlow ImmuneNet Backend`, database `connected`, websocket `available`, seed state `ready`. | None required. | None. |
| Demo reset endpoint on `127.0.0.1:8001` | Pass | `/demo/reset` returned `reset_complete`, 7 hubs, 8 edges, demo parcel `MED-104`. | None required. | None. |
| Sample route endpoint on `127.0.0.1:8001` | Pass | `/route/next-hop` selected `HUB-B` and full route `HUB-A -> HUB-B -> HUB-E -> CUSTOMER-ZONE`, final score `0.276`. | None required. | None. |
| Sample scan endpoint on `127.0.0.1:8001` | Pass | `/scan` returned `ACCEPTED`, `UPDATE_LOCATION`, LED `GREEN`, all immune checks `PASS`. | None required. | None. |
| Hardware scan endpoint on `127.0.0.1:8001` | Pass | `/hardware/scan` returned `hardware_scan_completed`, accepted `true`, LED `GREEN`, hardware context with scanner `ESP32-HUB-A-01`. | None required. | None. |

## Notes

- The port-8000 conflict is environmental, not a backend failure. The checked FastAPI app passed smoke checks on port 8001.
- Frontend `.env` currently points to `http://localhost:8000` and `ws://localhost:8000/ws`. If port 8000 remains occupied during demo, either free it or temporarily update frontend env to 8001.
- Existing uncommitted frontend visual changes and local SQLite/WAL files were present before this documentation pass; they should be resolved or intentionally ignored before final submission.
