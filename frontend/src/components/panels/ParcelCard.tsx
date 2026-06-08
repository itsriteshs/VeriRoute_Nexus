import type { ActiveParcel } from '../../types/packetflow';
import { formatTemperature } from '../../utils/formatters.ts';

type ParcelCardProps = {
  parcel: ActiveParcel;
};

export default function ParcelCard({ parcel }: ParcelCardProps) {
  const temperatureRisk = parcel.temperature_c > parcel.temperature_limit_c;
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
