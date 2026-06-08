import type {
  ActiveParcel,
  BadgeTone,
  CandidateScore,
  Edge,
  Hub,
  Metric,
  MovementProof,
  PanelPreview,
  Parcel,
  RelayStatus,
  RouteDecision,
} from '../types/packetflow';

export const sidebarItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Digital Twin', path: '/digital-twin' },
  { label: 'Parcels', path: '/parcels' },
  { label: 'Ledger', path: '/ledger' },
  { label: 'ImmuneNet', path: '/immunenet' },
  { label: 'Trust Board', path: '/trust-board' },
  { label: 'Demo Controls', path: '/demo-controls' },
];

export const topBarBadges: Array<{ label: string; tone: BadgeTone }> = [
  { label: 'Live Demo', tone: 'primary' },
  { label: 'Mock Data', tone: 'muted' },
  { label: 'Hardware Standby', tone: 'warning' },
];

export const relayStatus: RelayStatus = {
  title: 'SwarmFlow Relay',
  route: 'HUB-A ⇄ HUB-B',
  status: 'Standby',
};

export const metrics: Metric[] = [
  {
    label: 'Active Parcels',
    value: '24',
    description: 'Proof-ready consignments currently moving through trusted corridors.',
    meta: 'MED / COLD CHAIN',
    highlighted: true,
  },
  {
    label: 'Trusted Hubs',
    value: '18',
    description: 'Verified relay nodes above PacketFlow trust threshold.',
    meta: 'TRUST > 0.88',
  },
  {
    label: 'Anomalies Blocked',
    value: '7',
    description: 'Fake, clone, tamper, and cold-chain claims quarantined.',
    meta: '0 ACCEPTED RISK',
  },
  {
    label: 'Reroutes Triggered',
    value: '5',
    description: 'Trust-aware path changes prepared for live demo playback.',
    meta: '18 MIN SAVED',
  },
];

export const panels: PanelPreview[] = [
  {
    title: 'Digital Twin',
    eyebrow: 'Network canvas',
    description: 'A polished Phase 1 preview for hubs, parcels, route edges, and trust heat.',
    meta: 'HUB-A / HUB-B',
    tone: 'primary',
    variant: 'wide',
  },
  {
    title: 'PacketFlow Decision',
    eyebrow: 'Routing brain',
    description: 'Next-hop recommendation surface with confidence, proof level, and route state.',
    meta: 'NEXT HOP: HUB-B',
    tone: 'dark',
    variant: 'dark',
  },
  {
    title: 'ImmuneNet Alerts',
    eyebrow: 'Immune layer',
    description: 'Blocked scans, clone movement, temperature breach, and tamper signals.',
    meta: '7 BLOCKED',
    tone: 'warning',
  },
  {
    title: 'Movement Proof',
    eyebrow: 'Proof-of-Movement',
    description: 'GPS geofence, scanner identity, RFID, and temperature proof chain placeholder.',
    meta: 'RFID-DEMO-104',
    tone: 'muted',
  },
  {
    title: 'Hub Trust Board',
    eyebrow: 'Reputation layer',
    description: 'Trust ranking preview for healthy hubs, watch states, and recovery signals.',
    meta: '18 TRUSTED',
    tone: 'primary',
  },
  {
    title: 'Demo Controls',
    eyebrow: 'Operator console',
    description: 'Static Phase 1 control surface for future seed, reset, anomaly, and reroute flows.',
    meta: 'MOCK MODE',
    tone: 'dark',
  },
];

export const networkBars = [
  { label: 'HUB-A', value: 72, status: 'trusted' },
  { label: 'HUB-B', value: 58, status: 'watch' },
  { label: 'HUB-C', value: 86, status: 'trusted' },
  { label: 'HUB-D', value: 44, status: 'risk' },
  { label: 'HUB-E', value: 67, status: 'trusted' },
  { label: 'ZONE', value: 52, status: 'neutral' },
];

export const alertItems = [
  { title: 'Fake scan blocked', meta: 'MED-104 / HUB-C', severity: 'HIGH' },
  { title: 'Cold-chain watch', meta: '24.3C / LIMIT 25C', severity: 'WATCH' },
  { title: 'Clone claim quarantined', meta: 'RFID-DEMO-104', severity: 'BLOCKED' },
];

export const trustRows = [
  { hub: 'HUB-A', trust: '0.93', state: 'Trusted' },
  { hub: 'HUB-B', trust: '0.88', state: 'Standby' },
  { hub: 'HUB-C', trust: '0.74', state: 'Watch' },
  { hub: 'HUB-D', trust: '0.62', state: 'Reroute' },
];

export const twinHubs: Hub[] = [
  {
    id: 'HUB-A',
    name: 'Central Smart Hub A',
    trust_score: 0.98,
    trust_status: 'trusted',
    status: 'active',
    congestion: 0.16,
    cold_chain: false,
    hardware_live: true,
    anomaly_count: 0,
    routing_behavior: 'Origin smart hub; verifies MED-104 and initiates PacketFlow route.',
    trust_history: [0.96, 0.97, 0.98],
  },
  {
    id: 'HUB-B',
    name: 'Relay Hub B',
    trust_score: 0.92,
    trust_status: 'trusted',
    status: 'active',
    congestion: 0.22,
    cold_chain: false,
    hardware_live: true,
    anomaly_count: 1,
    routing_behavior: 'Preferred relay for active medicine route via ESP-NOW handoff.',
    trust_history: [0.91, 0.91, 0.92],
  },
  {
    id: 'HUB-C',
    name: 'Relay Hub C',
    trust_score: 0.5,
    trust_status: 'risky',
    status: 'active',
    congestion: 0.25,
    cold_chain: false,
    hardware_live: false,
    anomaly_count: 2,
    routing_behavior: 'Risky branch kept visible but avoided by active route.',
    trust_history: [0.58, 0.54, 0.5],
  },
  {
    id: 'COLD-HUB-C',
    name: 'Cold Chain Hub C',
    trust_score: 0.95,
    trust_status: 'trusted',
    status: 'active',
    congestion: 0.18,
    cold_chain: true,
    hardware_live: false,
    anomaly_count: 0,
    routing_behavior: 'Cold-chain recovery node for temperature-sensitive reroutes.',
    trust_history: [0.94, 0.95, 0.95],
  },
  {
    id: 'HUB-E',
    name: 'Final Relay Hub E',
    trust_score: 0.88,
    trust_status: 'trusted',
    status: 'active',
    congestion: 0.31,
    cold_chain: true,
    hardware_live: false,
    anomaly_count: 1,
    routing_behavior: 'Final relay before customer-zone delivery confirmation.',
    trust_history: [0.86, 0.87, 0.88],
  },
  {
    id: 'CUSTOMER-ZONE',
    name: 'Customer Delivery Zone',
    trust_score: 1,
    trust_status: 'trusted',
    status: 'active',
    congestion: 0.05,
    cold_chain: false,
    hardware_live: false,
    anomaly_count: 0,
    routing_behavior: 'Destination node; receives completed proof trail.',
    trust_history: [1, 1, 1],
  },
];

export const twinEdges: Edge[] = [
  { id: 'HUB-A-HUB-B', source: 'HUB-A', target: 'HUB-B', active: true, espNow: true, label: 'ESP-NOW handshake' },
  { id: 'HUB-A-HUB-C', source: 'HUB-A', target: 'HUB-C' },
  { id: 'HUB-B-HUB-E', source: 'HUB-B', target: 'HUB-E', active: true },
  { id: 'HUB-C-COLD-HUB-C', source: 'HUB-C', target: 'COLD-HUB-C' },
  { id: 'COLD-HUB-C-HUB-E', source: 'COLD-HUB-C', target: 'HUB-E' },
  { id: 'HUB-E-CUSTOMER-ZONE', source: 'HUB-E', target: 'CUSTOMER-ZONE', active: true },
];

export const twinParcel: Parcel = {
  id: 'MED-104',
  type: 'Medicine',
  current_hub: 'HUB-A',
  next_hop: 'HUB-B',
  status: 'Verified',
  temperature: '24.3°C',
};

export const activeParcel: ActiveParcel = {
  id: 'MED-104',
  type: 'Medicine',
  current_hub: 'HUB-A',
  previous_hub: null,
  next_hop: 'HUB-B',
  destination_hub: 'CUSTOMER-ZONE',
  priority: 'High',
  sla_minutes: 45,
  sla_remaining_min: 43,
  temperature_c: 24.3,
  temperature_limit_c: 25.0,
  carrier_type: 'Van',
  status: 'Verified movement',
  trust_state: 'Verified',
};

export const routeDecision: RouteDecision = {
  parcel_id: 'MED-104',
  current_hub: 'HUB-A',
  selected_next_hop: 'HUB-B',
  full_route: ['HUB-A', 'HUB-B', 'HUB-E', 'CUSTOMER-ZONE'],
  decision_type: 'Dynamic next-hop routing',
  triggered_by: 'Parcel creation / scan validation',
  reason: 'HUB-B selected because it preserves the 45-minute SLA while maintaining high trust.',
  timestamp: '10:42 AM demo time',
};

export const candidateScores: CandidateScore[] = [
  {
    hub_id: 'HUB-B',
    sla_risk: 0.2,
    congestion_risk: 0.5,
    trust_risk: 0.1,
    condition_risk: 0.4,
    cost_score: 0.3,
    final_score: 0.34,
    selected: true,
    result: 'Selected',
  },
  {
    hub_id: 'HUB-C',
    sla_risk: 0.2,
    congestion_risk: 0.2,
    trust_risk: 0.9,
    condition_risk: 0.2,
    cost_score: 0.32,
    final_score: 0.41,
    selected: false,
    result: 'Rejected: trust risk',
  },
  {
    hub_id: 'HUB-D',
    sla_risk: 0.5,
    congestion_risk: 0.2,
    trust_risk: 0.1,
    condition_risk: 0.2,
    cost_score: 0.35,
    final_score: 0.37,
    selected: false,
    result: 'Rejected: SLA risk',
  },
];

export const movementProof: MovementProof = {
  parcel_id: 'MED-104',
  hub_id: 'HUB-A',
  scanner_id: 'ESP32-HUB-A',
  rfid_verified: true,
  qr_verified: true,
  gps_distance_m: 18,
  geofence: 'PASS',
  temperature_c: 24.3,
  timestamp: '10:42 AM demo time',
  ble_verified: true,
  esp_now_prior_acceptance: true,
  esp_now_prior_hub: 'HUB-A',
  decision: 'ACCEPTED',
  led: 'GREEN',
  reason:
    'Movement accepted because identity, GPS geofence, route validity, temperature, and tamper checks passed.',
};
