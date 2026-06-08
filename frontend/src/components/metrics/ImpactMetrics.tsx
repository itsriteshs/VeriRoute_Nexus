import type { ImpactMetrics as ImpactMetricsType } from '../../types/packetflow';
import MetricDeltaBadge from './MetricDeltaBadge.tsx';

type ImpactMetricsProps = {
  metrics: ImpactMetricsType;
};

export default function ImpactMetrics({ metrics }: ImpactMetricsProps) {
  const items = [
    { label: 'Fake Scans Blocked', value: metrics.fakeScansBlocked, tone: 'danger' as const },
    { label: 'Cold-Chain Breaches', value: metrics.coldChainBreaches, tone: 'warning' as const },
    { label: 'Trust Quarantines', value: metrics.trustQuarantines, tone: 'danger' as const },
    { label: 'Scan Validation Latency', value: `${metrics.scanValidationLatencyMs}ms`, tone: 'info' as const },
    { label: 'Reroute Time', value: `${metrics.rerouteTimeMs}ms`, tone: 'success' as const },
  ];

  return (
    <section className="module-card impact-metrics">
      <div className="module-card__header">
        <div>
          <p>Impact Metrics</p>
          <h2>Demo Impact</h2>
        </div>
        <span className="mono-chip">LOCAL</span>
      </div>
      <div className="impact-metrics__hero">
        <div>
          <span>Active parcels</span>
          <strong>{metrics.activeParcels}</strong>
        </div>
        <div>
          <span>Trusted hubs</span>
          <strong>{metrics.trustedHubs}</strong>
        </div>
        <div>
          <span>Anomalies blocked</span>
          <strong>{metrics.anomaliesBlocked}</strong>
        </div>
        <div>
          <span>Reroutes triggered</span>
          <strong>{metrics.reroutesTriggered}</strong>
        </div>
      </div>
      <div className="impact-metrics__list">
        {items.map((item) => (
          <div key={item.label}>
            <span>{item.label}</span>
            <MetricDeltaBadge tone={item.tone} value={item.value} />
          </div>
        ))}
      </div>
    </section>
  );
}
