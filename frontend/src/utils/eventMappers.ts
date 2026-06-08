import type {
  DemoAlert,
  ImmuneCheckResult,
  ImmuneCheckStatus,
  LedgerEvent,
} from '../types/packetflow';
import { getDemoTimestamp } from './demoActions.ts';

const pass = 'PASS' satisfies ImmuneCheckStatus;
const fail = 'FAIL' satisfies ImmuneCheckStatus;
const skipped = 'SKIPPED' satisfies ImmuneCheckStatus;

export const acceptedScanChecks: ImmuneCheckResult[] = [
  { key: 'rfid', label: 'RFID', status: pass },
  { key: 'qr', label: 'QR', status: pass },
  { key: 'geofence', label: 'GPS geofence', status: pass },
  { key: 'temperature', label: 'Temperature', status: pass, detail: '24.3C / 25C' },
  { key: 'ble', label: 'BLE', status: pass },
  { key: 'esp_now', label: 'ESP-NOW', status: pass },
];

export const fakeScanChecks: ImmuneCheckResult[] = [
  { key: 'geofence', label: 'Geofence', status: fail },
  { key: 'speed', label: 'Speed', status: pass },
  { key: 'route_graph', label: 'Route graph', status: pass },
  { key: 'clone_scan', label: 'Clone scan', status: pass },
  { key: 'cold_chain', label: 'Cold-chain', status: pass },
  { key: 'tamper', label: 'Tamper', status: pass },
];

export const coldChainChecks: ImmuneCheckResult[] = [
  { key: 'temperature', label: 'Temperature', status: fail, detail: '29.2C' },
  { key: 'cold_chain', label: 'Limit', status: fail, detail: '25C' },
  { key: 'route_graph', label: 'New route', status: pass, detail: 'Includes COLD-HUB-C' },
];

export const p2pChecks: ImmuneCheckResult[] = [
  { key: 'esp_now', label: 'ESP-NOW', status: pass },
  { key: 'route_graph', label: 'Route graph', status: pass },
  { key: 'rfid', label: 'RFID', status: skipped },
];

export const rerouteChecks: ImmuneCheckResult[] = [
  { key: 'route_graph', label: 'Route graph', status: pass },
  { key: 'speed', label: 'SLA speed', status: pass },
  { key: 'cold_chain', label: 'Cold-chain option', status: pass },
];

export function createLedgerEvent(
  input: Omit<
    LedgerEvent,
    'id' | 'timestamp' | 'geofence' | 'speed' | 'routeGraph' | 'clone' | 'coldChain' | 'tamper'
  > & {
    id: string;
    timestamp?: string;
    checks?: Partial<
      Pick<LedgerEvent, 'geofence' | 'speed' | 'routeGraph' | 'clone' | 'coldChain' | 'tamper'>
    >;
  },
): LedgerEvent {
  return {
    id: input.id,
    timestamp: input.timestamp ?? getDemoTimestamp(),
    parcelId: input.parcelId,
    hubId: input.hubId,
    event: input.event,
    category: input.category,
    geofence: input.checks?.geofence ?? skipped,
    speed: input.checks?.speed ?? skipped,
    routeGraph: input.checks?.routeGraph ?? skipped,
    clone: input.checks?.clone ?? skipped,
    coldChain: input.checks?.coldChain ?? skipped,
    tamper: input.checks?.tamper ?? skipped,
    decision: input.decision,
    action: input.action,
    reason: input.reason,
  };
}

export function attachAuditDetails(alert: DemoAlert, event: LedgerEvent): DemoAlert {
  return {
    ...alert,
    ledgerEventId: event.id,
  };
}
