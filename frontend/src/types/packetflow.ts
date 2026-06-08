export type BadgeTone = 'primary' | 'dark' | 'muted' | 'warning';

export type Metric = {
  label: string;
  value: string;
  description: string;
  meta: string;
  delta?: string;
  highlighted?: boolean;
};

export type PanelPreview = {
  title: string;
  eyebrow: string;
  description: string;
  meta: string;
  tone: BadgeTone;
  variant?: 'dark' | 'wide';
};

export type RelayStatus = {
  title: string;
  route: string;
  status: string;
};

export type TrustStatus = 'trusted' | 'watch' | 'risky' | 'quarantined';

export type HubStatus = 'active' | 'failed' | 'overloaded';

export type Hub = {
  id: string;
  name: string;
  trust_score: number;
  trust_status: TrustStatus;
  status: HubStatus;
  congestion: number;
  cold_chain: boolean;
  hardware_live: boolean;
  anomaly_count: number;
  routing_behavior: string;
  trust_history?: number[];
};

export type Edge = {
  id: string;
  source: string;
  target: string;
  active?: boolean;
  espNow?: boolean;
  label?: string;
};

export type Parcel = {
  id: string;
  type: string;
  current_hub: string;
  next_hop: string;
  status: string;
  temperature: string;
};

export type ActiveParcel = {
  id: string;
  type: string;
  current_hub: string;
  previous_hub: string | null;
  next_hop: string;
  destination_hub: string;
  priority: string;
  sla_minutes: number;
  sla_remaining_min: number;
  temperature_c: number;
  temperature_limit_c: number;
  carrier_type: string;
  status: string;
  trust_state: string;
};

export type RouteDecision = {
  parcel_id: string;
  current_hub: string;
  selected_next_hop: string;
  full_route: string[];
  decision_type: string;
  triggered_by: string;
  reason: string;
  timestamp: string;
};

export type CandidateScore = {
  hub_id: string;
  sla_risk: number;
  congestion_risk: number;
  trust_risk: number;
  condition_risk: number;
  cost_score: number;
  final_score: number;
  selected: boolean;
  result: string;
};

export type RiskFactor = {
  key: keyof Pick<CandidateScore, 'sla_risk' | 'congestion_risk' | 'trust_risk' | 'condition_risk' | 'cost_score'>;
  label: string;
  value: number;
  weight: number;
  status?: string;
};

export type MovementProof = {
  parcel_id: string;
  hub_id: string;
  scanner_id: string;
  rfid_verified: boolean;
  qr_verified: boolean;
  gps_distance_m: number;
  geofence: 'PASS' | 'FAIL';
  temperature_c: number;
  timestamp: string;
  ble_verified: boolean;
  esp_now_prior_acceptance: boolean;
  esp_now_prior_hub: string;
  decision: 'ACCEPTED' | 'BLOCKED';
  led: 'GREEN' | 'RED' | 'AMBER';
  reason: string;
};

export type DemoAlertType = 'accepted' | 'blocked' | 'rerouted' | 'p2p' | 'trust_update' | 'cold_chain' | 'agentops';

export type ImmuneCheckStatus = 'PASS' | 'FAIL' | 'WARN' | 'SKIPPED';

export type ImmuneCheckKey =
  | 'geofence'
  | 'speed'
  | 'route_graph'
  | 'clone_scan'
  | 'cold_chain'
  | 'tamper'
  | 'rfid'
  | 'qr'
  | 'ble'
  | 'esp_now'
  | 'temperature';

export type ImmuneCheckResult = {
  key: ImmuneCheckKey;
  label: string;
  status: ImmuneCheckStatus;
  detail?: string;
};

export type DemoAlert = {
  id: string;
  type: DemoAlertType;
  status: string;
  title: string;
  parcelId?: string;
  hubId?: string;
  failedCheck?: string;
  actionTaken?: string;
  reason: string;
  timestamp: string;
  severity: 'success' | 'warning' | 'danger' | 'info';
  decision?: string;
  trustDelta?: number;
  routeChange?: string[];
  checks?: ImmuneCheckResult[];
  ledgerEventId?: string;
};

export type LedgerEvent = {
  id: string;
  timestamp: string;
  parcelId?: string;
  hubId?: string;
  event: string;
  category: DemoAlertType;
  geofence: ImmuneCheckStatus;
  speed: ImmuneCheckStatus;
  routeGraph: ImmuneCheckStatus;
  clone: ImmuneCheckStatus;
  coldChain: ImmuneCheckStatus;
  tamper: ImmuneCheckStatus;
  decision: string;
  action: string;
  reason: string;
};

export type ImpactMetrics = {
  activeParcels: number;
  trustedHubs: number;
  anomaliesBlocked: number;
  reroutesTriggered: number;
  fakeScansBlocked: number;
  coldChainBreaches: number;
  trustQuarantines: number;
  scanValidationLatencyMs: number;
  rerouteTimeMs: number;
};

export type AgentOpsEvent = {
  title: string;
  detail: string;
  timestamp: string;
} | null;

export type ColdChainState = {
  current_temperature_c: number;
  limit_c: number;
  status: string;
  action: string;
} | null;

export type GraphPoint = {
  x: number;
  y: number;
};
