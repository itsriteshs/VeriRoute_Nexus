import { Play, RotateCcw } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import DemoEventToast from '../components/demo/DemoEventToast.tsx';
import DemoTimeline from '../components/demo/DemoTimeline.tsx';
import PacketFlowDecision from '../components/panels/PacketFlowDecision.tsx';
import ParcelCard from '../components/panels/ParcelCard.tsx';
import DigitalTwin from '../components/twin/DigitalTwin.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type DashboardProps = {
  demo: DemoState;
};

export default function Dashboard({ demo }: DashboardProps) {
  const runDemo = () => {
    void demo.acceptScan();
  };

  return (
    <main className="dashboard">
      <DemoEventToast message={demo.toast} />
      <section className="dashboard-header">
        <div>
          <p className="eyebrow">Proof network / Phase 1 shell</p>
          <h1>PacketFlow Command Center</h1>
          <p className="dashboard-header__subtitle">
            Proof-of-Movement, trust-aware routing, and live logistics immunity.
          </p>
        </div>

        <div className="dashboard-header__actions">
          <button className="button button--primary" onClick={runDemo} type="button">
            <Play size={17} strokeWidth={2} />
            Run Demo
          </button>
          <button className="button button--secondary" onClick={demo.resetDemo} type="button">
            <RotateCcw size={17} strokeWidth={2} />
            Reset State
          </button>
        </div>
      </section>

      <section className="metric-grid" aria-label="PacketFlow metrics">
        {demo.metrics.map((metric) => (
          <MetricCard key={metric.label} metric={metric} />
        ))}
      </section>

      <section className="command-grid command-grid--overview" aria-label="PacketFlow overview modules">
        <div className="overview-twin">
          <DigitalTwin
            activeRoute={demo.activeRoute}
            edges={demo.edges}
            hubs={demo.hubs}
            pulseHandshake={demo.pulseHandshake}
            selectedParcel={demo.parcel}
          />
        </div>

        <div className="right-demo-stack">
          <ParcelCard parcel={demo.parcel} />
          <PacketFlowDecision routeDecision={demo.routeDecision} />
        </div>

        <DemoTimeline alerts={demo.alerts} />
      </section>
    </main>
  );
}
