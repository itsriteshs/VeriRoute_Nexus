import type { ActiveParcel } from '../../types/packetflow';
import { formatTemperature } from '../../utils/formatters.ts';

type ParcelCardProps = {
  parcel: ActiveParcel;
};

export default function ParcelCard({ parcel }: ParcelCardProps) {
  const temperatureRisk = parcel.temperature_c > parcel.temperature_limit_c;
  const slaProgress = Math.max(0, Math.min(100, (parcel.sla_remaining_min / parcel.sla_minutes) * 100));
  const temperatureProgress = Math.max(0, Math.min(100, (parcel.temperature_c / parcel.temperature_limit_c) * 100));
  const rows = [
    ['Current hub', parcel.current_hub],
    ['Previous hub', parcel.previous_hub ?? 'None'],
    ['Next hop', parcel.next_hop],
    ['Destination', parcel.destination_hub],
    ['SLA remaining', `${parcel.sla_remaining_min} min`],
    ['Temperature', `${formatTemperature(parcel.temperature_c)} / ${formatTemperature(parcel.temperature_limit_c)}`],
    ['Carrier', parcel.carrier_type],
    ['Trust state', parcel.trust_state],
  ];

  return (
    <section className="module-card demo-panel parcel-card">
      <div className="module-card__header">
        <div>
          <p>Selected Parcel</p>
          <h2>{parcel.id}</h2>
        </div>
        <span className={`mono-chip ${temperatureRisk ? 'mono-chip--warning' : ''}`}>{parcel.status}</span>
      </div>

      <div className="parcel-card__badges">
        <span>{parcel.type} parcel</span>
        <span>Priority {parcel.priority}</span>
        <span>{parcel.trust_state}</span>
      </div>

      <div className="parcel-card__signal-grid">
        <div>
          <span>SLA reserve</span>
          <strong>{parcel.sla_remaining_min} / {parcel.sla_minutes} min</strong>
          <i style={{ width: `${slaProgress}%` }} />
        </div>
        <div className={temperatureRisk ? 'is-warning' : ''}>
          <span>Thermal load</span>
          <strong>{formatTemperature(parcel.temperature_c)} / {formatTemperature(parcel.temperature_limit_c)}</strong>
          <i style={{ width: `${temperatureProgress}%` }} />
        </div>
      </div>

      <dl className="parcel-card__grid">
        {rows.map(([label, value]) => (
          <div className={label === 'Temperature' && temperatureRisk ? 'is-warning' : ''} key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
