import type { Hub } from '../../types/packetflow';
import TrustRow from './TrustRow.tsx';

type TrustBoardProps = {
  hubs: Hub[];
};

export default function TrustBoard({ hubs }: TrustBoardProps) {
  return (
    <section className="module-card trust-board">
      <div className="module-card__header">
        <div>
          <p>Reputation Layer</p>
          <h2>Hub Trust Board</h2>
        </div>
        <span className="mono-chip">{hubs.length} HUBS</span>
      </div>

      <div className="trust-board__table">
        <div className="trust-row trust-row--head">
          <span>Hub</span>
          <span>Trust score</span>
          <span>Status</span>
          <span>Anomalies</span>
          <span>Routing behavior</span>
          <span>History</span>
        </div>
        {hubs.map((hub) => (
          <TrustRow hub={hub} key={hub.id} />
        ))}
      </div>
    </section>
  );
}
