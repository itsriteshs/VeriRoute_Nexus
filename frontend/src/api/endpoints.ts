// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: API endpoint route definitions.

export const endpoints = {
  health: '/health',
  ready: '/ready',
  seed: '/demo/seed',
  reset: '/demo/reset',
  snapshot: '/demo/snapshot',
  validate: '/demo/validate',
  runMainWow: '/demo/run/main-wow',
  hubs: '/hubs',
  edges: '/edges',
  parcels: '/parcels',
  nextHop: '/route/next-hop',
  scan: '/scan',
  hardwareScan: '/hardware/scan',
  fakeScan: '/scan/fake',
  cloneScan: '/scan/clone',
  tamperScan: '/scan/tamper',
  failHub: '/scenario/fail-hub',
  overloadHub: '/scenario/overload-hub',
  trafficJam: '/scenario/traffic-jam',
  weatherRisk: '/scenario/weather-risk',
  tempBreach: '/scenario/temp-breach',
  p2pHandshake: '/hardware/p2p-handshake',
  metrics: '/metrics',
  wsStatus: '/ws/status'
};
