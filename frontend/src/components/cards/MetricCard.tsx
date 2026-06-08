import { ArrowUpRight } from 'lucide-react';
import type { Metric } from '../../types/packetflow';

type MetricCardProps = {
  metric: Metric;
};

export default function MetricCard({ metric }: MetricCardProps) {
  return (
    <article className={`metric-card ${metric.highlighted ? 'metric-card--highlighted' : ''}`}>
      <div className="metric-card__top">
        <p className="metric-card__label">{metric.label}</p>
        <span className="metric-card__icon" aria-hidden="true">
          <ArrowUpRight size={16} strokeWidth={1.9} />
        </span>
      </div>
      <p className="metric-card__value">{metric.value}</p>
      <p className="metric-card__description">{metric.description}</p>
      <p className="metric-card__meta">{metric.meta}</p>
    </article>
  );
}
