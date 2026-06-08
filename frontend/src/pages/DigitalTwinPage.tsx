import MetricCard from '../components/cards/MetricCard';
import PacketFlowDecision from '../components/panels/PacketFlowDecision.tsx';
import ScoreBreakdown from '../components/panels/ScoreBreakdown.tsx';
import DigitalTwin from '../components/twin/DigitalTwin.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type DigitalTwinPageProps = {
  demo: DemoState;
};

export default function DigitalTwinPage({ demo }: DigitalTwinPageProps) {
  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Network Twin / Route Intelligence</p>
          <h1>Digital Twin</h1>
          <p>Watch hubs, trust states, proof handoffs, and route changes as one PacketFlow network.</p>
        </div>
        <span className="mono-chip">{demo.activeRoute.join(' -> ')}</span>
      </section>

      <section className="metric-grid" aria-label="Digital Twin summary">
        {demo.metrics.map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </section>

      <section className="command-grid" aria-label="Digital Twin modules">
        <DigitalTwin
          activeRoute={demo.activeRoute}
          edges={demo.edges}
          hubs={demo.hubs}
          pulseHandshake={demo.pulseHandshake}
          selectedParcel={demo.parcel}
        />
        <PacketFlowDecision routeDecision={demo.routeDecision} />
        <ScoreBreakdown candidateScores={demo.candidateScores} />
      </section>
    </main>
  );
}
