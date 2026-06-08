import type { Hub } from '../../types/packetflow';
import { formatScore } from '../../utils/formatters.ts';
import TrustBadge from './TrustBadge.tsx';
import TrustSparkline from './TrustSparkline.tsx';

type TrustRowProps = {
  hub: Hub;
};

export default function TrustRow({ hub }: TrustRowProps) {
  return (
    <div className="trust-row">
      <div>
        <strong>{hub.id}</strong>
        <small>{hub.name}</small>
      </div>
      <span>{formatScore(hub.trust_score)}</span>
      <TrustBadge status={hub.trust_status} />
      <span>{hub.anomaly_count}</span>
      <p>{hub.routing_behavior}</p>
      <TrustSparkline values={hub.trust_history} />
    </div>
  );
}
