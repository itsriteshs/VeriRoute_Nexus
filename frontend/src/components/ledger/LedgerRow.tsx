import type { ImmuneCheckStatus, LedgerEvent } from '../../types/packetflow';

type LedgerRowProps = {
  event: LedgerEvent;
};

function CheckCell({ status }: { status: ImmuneCheckStatus }) {
  return <span className={`ledger-check ledger-check--${status.toLowerCase()}`}>{status}</span>;
}

export default function LedgerRow({ event }: LedgerRowProps) {
  return (
    <div className="ledger-row">
      <span>{event.timestamp}</span>
      <strong>{event.parcelId ?? 'N/A'}</strong>
      <strong>{event.hubId ?? 'N/A'}</strong>
      <span>{event.event}</span>
      <CheckCell status={event.geofence} />
      <CheckCell status={event.speed} />
      <CheckCell status={event.routeGraph} />
      <CheckCell status={event.clone} />
      <CheckCell status={event.coldChain} />
      <CheckCell status={event.tamper} />
      <span>{event.decision}</span>
      <span>{event.action}</span>
      <p>{event.reason}</p>
    </div>
  );
}
