import type { DemoAlert } from '../../types/packetflow';
import AlertDetailPanel from './AlertDetailPanel.tsx';
import AlertCard from './AlertCard';

type ImmuneNetAlertsProps = {
  alerts: DemoAlert[];
  selectedAlert: DemoAlert | null;
  onSelectAlert: (alert: DemoAlert) => void;
};

const baselineAlerts: DemoAlert[] = [
  {
    id: 'baseline-fake',
    type: 'blocked',
    status: 'WATCH',
    title: 'Geofence check armed',
    parcelId: 'MED-104',
    hubId: 'HUB-C',
    reason: 'ImmuneNet is ready to quarantine impossible movement claims.',
    actionTaken: 'ARM_GEOFENCE_CHECKS',
    timestamp: 'Baseline',
    severity: 'info',
    decision: 'READY',
  },
];

export default function ImmuneNetAlerts({ alerts, selectedAlert, onSelectAlert }: ImmuneNetAlertsProps) {
  const visibleAlerts = alerts.length > 0 ? alerts : baselineAlerts;
  const activeAlert = selectedAlert ?? visibleAlerts[0] ?? null;

  return (
    <section className="module-card module-card--alerts">
      <div className="module-card__header">
        <div>
          <p>Immune Layer</p>
          <h2>ImmuneNet Alerts</h2>
        </div>
        <span className="mono-chip">{alerts.length || 1} ACTIVE</span>
      </div>
      <div className="alert-audit-layout">
        <div className="alert-card-list">
          {visibleAlerts.map((alert) => (
            <AlertCard
              alert={alert}
              isSelected={activeAlert?.id === alert.id}
              key={alert.id}
              onSelect={onSelectAlert}
            />
          ))}
        </div>
        <AlertDetailPanel alert={activeAlert} />
      </div>
    </section>
  );
}
