import type { ActiveParcel, Hub } from '../../types/packetflow';

type HubDetailPopoverProps = {
  hub: Hub;
  parcel: ActiveParcel;
  activeRoute: string[];
};

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export default function HubDetailPopover({ hub, parcel, activeRoute }: HubDetailPopoverProps) {
  const routeIndex = activeRoute.indexOf(hub.id);
  const routeRole =
    hub.id === parcel.current_hub
      ? 'Current scan location'
      : hub.id === parcel.next_hop
        ? 'Authorised next hop'
        : hub.id === parcel.destination_hub
          ? 'Destination zone'
          : routeIndex >= 0
            ? `Route step ${routeIndex + 1}`
            : 'Standby node';
  const rows = [
    ['Role', routeRole],
    ['Trust', hub.trust_score.toFixed(2)],
    ['Reputation', hub.trust_status],
    ['Ops status', hub.status],
    ['Congestion', formatPercent(hub.congestion)],
    ['Cold chain', hub.cold_chain ? 'Available' : 'No'],
    ['Hardware', hub.hardware_live ? 'Live' : 'Offline'],
    ['Anomalies', String(hub.anomaly_count)],
  ];

  return (
    <aside className="hub-detail">
      <div className="hub-detail__top">
        <p>Selected node</p>
        <strong>{hub.name}</strong>
        <span>{hub.id}</span>
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
