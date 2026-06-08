import type { Hub } from '../../types/packetflow';

type HubDetailPopoverProps = {
  hub: Hub;
};

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export default function HubDetailPopover({ hub }: HubDetailPopoverProps) {
  const rows = [
    ['Hub ID', hub.id],
    ['Trust Score', hub.trust_score.toFixed(2)],
    ['Trust Status', hub.trust_status],
    ['Status', hub.status],
    ['Congestion', formatPercent(hub.congestion)],
    ['Cold Chain', hub.cold_chain ? 'Available' : 'No'],
    ['Hardware Live', hub.hardware_live ? 'Yes' : 'No'],
    ['Anomalies', String(hub.anomaly_count)],
  ];

  return (
    <aside className="hub-detail">
      <div className="hub-detail__top">
        <p>Selected Hub</p>
        <strong>{hub.name}</strong>
      </div>
      <dl>
        {rows.map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
      <p className="hub-detail__behavior">{hub.routing_behavior}</p>
    </aside>
  );
}
