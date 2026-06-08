import type { DemoAlert } from '../../types/packetflow';
import ImmuneCheckTrace from './ImmuneCheckTrace.tsx';

type AlertDetailPanelProps = {
  alert: DemoAlert | null;
};

export default function AlertDetailPanel({ alert }: AlertDetailPanelProps) {
  if (!alert) {
    return (
      <aside className="alert-detail alert-detail--empty">
        <span className="mono-chip">DETAIL</span>
        <p>Select an alert to inspect its trust decision, action, ledger event, and check trace.</p>
      </aside>
    );
  }

  return (
    <aside className={`alert-detail alert-detail--${alert.severity}`}>
      <div className="alert-detail__top">
        <span>{alert.status}</span>
        <strong>{alert.title}</strong>
        <small>{alert.timestamp}</small>
      </div>

      <dl className="alert-detail__grid">
        <div>
          <dt>Decision</dt>
          <dd>{alert.decision ?? alert.status}</dd>
        </div>
        <div>
          <dt>Parcel</dt>
          <dd>{alert.parcelId ?? 'N/A'}</dd>
        </div>
        <div>
          <dt>Hub</dt>
          <dd>{alert.hubId ?? 'N/A'}</dd>
        </div>
        <div>
          <dt>Action</dt>
          <dd>{alert.actionTaken ?? 'MONITOR_EVENT'}</dd>
        </div>
        <div>
          <dt>Failed check</dt>
          <dd>{alert.failedCheck ?? 'None'}</dd>
        </div>
        <div>
          <dt>Trust delta</dt>
          <dd>{typeof alert.trustDelta === 'number' ? alert.trustDelta.toFixed(2) : 'N/A'}</dd>
        </div>
        <div>
          <dt>Ledger</dt>
          <dd>{alert.ledgerEventId ?? 'Pending'}</dd>
        </div>
      </dl>

      {alert.routeChange ? (
        <div className="alert-detail__route">
          <span>Route change</span>
          <p>{alert.routeChange.join(' -> ')}</p>
        </div>
      ) : null}

      <p className="alert-detail__reason">{alert.reason}</p>
      <ImmuneCheckTrace checks={alert.checks} />
    </aside>
  );
}
