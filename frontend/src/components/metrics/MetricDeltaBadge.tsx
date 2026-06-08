type MetricDeltaBadgeProps = {
  value: number | string;
  tone?: 'success' | 'warning' | 'danger' | 'info';
};

export default function MetricDeltaBadge({ value, tone = 'success' }: MetricDeltaBadgeProps) {
  return <span className={`metric-delta metric-delta--${tone}`}>{value}</span>;
}
