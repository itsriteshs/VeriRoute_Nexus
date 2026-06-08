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
  fakeScan: '/scan/fake',
  failHub: '/scenario/fail-hub',
  overloadHub: '/scenario/overload-hub',
  tempBreach: '/scenario/temp-breach',
  p2pHandshake: '/hardware/p2p-handshake',
  metrics: '/metrics',
  wsStatus: '/ws/status'
};
