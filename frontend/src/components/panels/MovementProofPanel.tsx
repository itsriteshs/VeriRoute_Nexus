import type { MovementProof } from '../../types/packetflow';
import { formatBoolean, formatTemperature } from '../../utils/formatters.ts';

type MovementProofPanelProps = {
  movementProof: MovementProof;
};

export default function MovementProofPanel({ movementProof }: MovementProofPanelProps) {
  const blocked = movementProof.decision === 'BLOCKED';
  const checks = [
    ['RFID', formatBoolean(movementProof.rfid_verified)],
    ['QR', formatBoolean(movementProof.qr_verified)],
    ['GPS distance', `${movementProof.gps_distance_m}m from ${movementProof.hub_id}`],
    ['Geofence', movementProof.geofence],
    ['Temperature', formatTemperature(movementProof.temperature_c)],
    ['BLE', formatBoolean(movementProof.ble_verified)],
    ['ESP-NOW', `Pre-authorised by ${movementProof.esp_now_prior_hub}`],
    ['LED', movementProof.led],
  ];

  return (
    <section className="module-card demo-panel proof-panel">
      <div className="module-card__header">
        <div>
          <p>Hardware Proof</p>
          <h2>Movement Proof</h2>
        </div>
        <span className={`mono-chip ${blocked ? 'mono-chip--danger' : ''}`}>{movementProof.decision}</span>
      </div>

      <div className="proof-panel__top">
        <span>SmartHub scan</span>
        <strong>{movementProof.scanner_id}</strong>
        <em>Edge verification</em>
      </div>

      <dl className="proof-checks">
        {checks.map(([label, value]) => (
          <div className={(label === 'Geofence' && movementProof.geofence === 'FAIL') || label === 'LED' && movementProof.led === 'RED' ? 'is-danger' : ''} key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>

      <p className="module-card__copy">{movementProof.reason}</p>
      <p className="proof-panel__timestamp">{movementProof.timestamp}</p>
    </section>
  );
}
