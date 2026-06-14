# Screenshots To Add

Add final screenshots here before submission:

1. `dashboard-overview.png` - dashboard with backend live and route decision visible.
2. `digital-twin.png` - hub graph and active parcel route.
3. `fake-scan-blocked.png` - ImmuneNet blocked fake scan alert.
4. `cold-chain-breach.png` - temperature breach and cold-chain reroute.
5. `trust-ledger.png` - ledger or trust board showing proof and trust score changes.
6. `api-docs.png` - FastAPI docs at `http://localhost:8000/docs`.
7. `hardware-setup.png` - physical SmartHub setup or hardware simulator.

Screenshots should be taken after running:

```bash
curl -X POST http://localhost:8000/demo/reset
```

Then trigger normal scan, fake scan, and temperature breach so the UI contains the proof states judges need to see.
