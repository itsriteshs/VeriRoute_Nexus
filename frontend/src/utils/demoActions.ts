import type { DemoAlert, DemoAlertType } from '../types/packetflow';

let alertSequence = 0;

export function getDemoTimestamp() {
  return '10:42 AM demo time';
}

export function createDemoAlert(input: {
  type: DemoAlertType;
  status: string;
  title: string;
  reason: string;
  severity: DemoAlert['severity'];
  parcelId?: string;
  hubId?: string;
  failedCheck?: DemoAlert['failedCheck'];
  actionTaken?: DemoAlert['actionTaken'];
  decision?: DemoAlert['decision'];
  trustDelta?: DemoAlert['trustDelta'];
  routeChange?: DemoAlert['routeChange'];
  checks?: DemoAlert['checks'];
  ledgerEventId?: DemoAlert['ledgerEventId'];
}): DemoAlert {
  alertSequence += 1;

  return {
    id: `demo-alert-${alertSequence}`,
    timestamp: getDemoTimestamp(),
    ...input,
  };
}
