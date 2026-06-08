import type { TrustStatus } from '../../types/packetflow';

type TrustBadgeProps = {
  status: TrustStatus;
};

export default function TrustBadge({ status }: TrustBadgeProps) {
  return <span className={`trust-badge trust-badge--${status}`}>{status}</span>;
}
