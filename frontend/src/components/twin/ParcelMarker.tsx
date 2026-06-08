import type { ActiveParcel } from '../../types/packetflow';
import { getParcelPosition } from '../../utils/graphLayout.ts';
import { formatTemperature } from '../../utils/formatters.ts';

type ParcelMarkerProps = {
  parcel: ActiveParcel;
};

export default function ParcelMarker({ parcel }: ParcelMarkerProps) {
  const position = getParcelPosition(parcel.current_hub, parcel.next_hop);

  return (
    <g className="parcel-marker" transform={`translate(${position.x} ${position.y})`}>
      <rect height="54" rx="18" width="132" x="-66" y="-27" />
      <text className="parcel-marker__id" textAnchor="middle" y="-3">
        {parcel.id}
      </text>
      <text className="parcel-marker__meta" textAnchor="middle" y="16">
        {parcel.trust_state} / {formatTemperature(parcel.temperature_c)}
      </text>
    </g>
  );
}
