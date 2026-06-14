# Submission Checklist

## GitHub Readiness

- [ ] Root README starts with PacketFlow ImmuneNet and one-line pitch.
- [ ] Real/simulated/hardware-ready/future boundaries are visible.
- [ ] No secrets are committed.
- [ ] Local DB artifacts such as `*.db-wal`, `*.db-shm`, stale DB backups, and caches are removed or ignored.
- [ ] Repo opens cleanly from a fresh clone.
- [ ] Branch is pushed and GitHub renders Mermaid diagrams.

## README Completeness

- [x] Project title and pitch.
- [x] 30-second explanation.
- [x] Problem and solution.
- [x] Architecture diagram.
- [x] API route table.
- [x] Setup and env variables.
- [x] Demo scenarios.
- [x] Scalability, privacy, fallback plan.
- [x] Final judge line.

## Demo Video Checklist

- [ ] Start at dashboard with backend live.
- [ ] Show WebSocket connected or live updates.
- [ ] Show normal scan accepted.
- [ ] Show fake scan blocked.
- [ ] Show cold-chain breach reroute.
- [ ] Show trust/ledger proof.
- [ ] Show hardware simulator or physical hardware.
- [ ] End with "We are not tracking parcels. We are proving movement."

## Screenshots Checklist

- [ ] Dashboard overview.
- [ ] Digital twin.
- [ ] Fake scan blocked.
- [ ] Cold-chain breach.
- [ ] Trust ledger.
- [ ] API docs.
- [ ] Hardware setup/simulator.

## Build/Test Checklist

- [ ] `python3 -m compileall -q backend`
- [ ] `cd backend && pytest`
- [ ] `cd frontend && npm run typecheck`
- [ ] `cd frontend && npm run build`
- [ ] Backend health check.
- [ ] Demo reset endpoint.
- [ ] Valid scan endpoint.
- [ ] Route endpoint.
- [ ] Hardware scan endpoint.
- [ ] Browser click-through.

## Docs Checklist

- [x] `docs/REPO_AUDIT.md`
- [x] `docs/JUDGE_EVALUATION.md`
- [x] `docs/ARCHITECTURE.md`
- [x] `docs/API.md`
- [x] `docs/DEMO_GUIDE.md`
- [x] `docs/SIMULATION.md`
- [x] `docs/HARDWARE.md`
- [x] `docs/FEATURE_STATUS.md`
- [x] `docs/VERIFICATION_LOG.md`
- [x] `docs/NAMING_AND_POSITIONING.md`

## Judge Scoring Checklist

- [x] Theme fit is obvious.
- [x] Innovation is named and differentiated.
- [x] Technical depth is evidenced in files.
- [x] Engineering quality is backed by tests.
- [ ] Frontend is visually verified and captured.
- [x] API is documented.
- [x] Simulation boundary is honest.
- [x] Hardware readiness is documented.
- [x] Fallback plan is explicit.
- [ ] Final video/screenshots are committed or linked.

## Final Round 1 Submission Checklist

- [ ] Update GitHub description.
- [ ] Add demo video link.
- [ ] Add screenshots.
- [ ] Verify clean clone run.
- [ ] Re-run verification commands.
- [ ] Confirm no stale project names in deck.
- [ ] Submit repository and video.
