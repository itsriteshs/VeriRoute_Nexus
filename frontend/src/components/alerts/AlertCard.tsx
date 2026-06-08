import type { DemoAlert } from '../../types/packetflow';

type AlertCardProps = {
  alert: DemoAlert;
  isSelected?: boolean;
  onSelect?: (alert: DemoAlert) => void;
};

export default function AlertCard({ alert, isSelected = false, onSelect }: AlertCardProps) {
  return (
    <button
      className={`alert-card alert-card--${alert.severity} ${isSelected ? 'is-selected' : ''}`}
      onClick={() => onSelect?.(alert)}
      type="button"
    >
      <i className="alert-card__dot" aria-hidden="true" />
      <span>{alert.status}</span>
      <div>
        <strong>{alert.title}</strong>
        <small>
          {[alert.parcelId, alert.hubId].filter(Boolean).join(' / ')} · {alert.timestamp}
        </small>
        <small>{alert.failedCheck ? `Failed: ${alert.failedCheck}` : alert.actionTaken ?? 'Audit trace ready'}</small>
        <p>{alert.reason}</p>
      </div>
    </button>
  );
}
