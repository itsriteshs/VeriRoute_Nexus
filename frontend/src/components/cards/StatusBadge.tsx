import type { BadgeTone } from '../../types/packetflow';

type StatusBadgeProps = {
  label: string;
  tone?: BadgeTone;
};

export default function StatusBadge({ label, tone = 'primary' }: StatusBadgeProps) {
  return <span className={`status-badge status-badge--${tone}`}>{label}</span>;
}
