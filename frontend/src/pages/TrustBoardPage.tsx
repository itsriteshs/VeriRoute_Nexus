import ImpactMetrics from '../components/metrics/ImpactMetrics.tsx';
import PacketFlowDecision from '../components/panels/PacketFlowDecision.tsx';
import TrustBoard from '../components/trust/TrustBoard.tsx';
import DigitalTwin from '../components/twin/DigitalTwin.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type TrustBoardPageProps = {
  demo: DemoState;
};

export default function TrustBoardPage({ demo }: TrustBoardPageProps) {
  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Reputation Layer / Routing Variable</p>
          <h1>Trust Board</h1>
          <p>Track hub trust scores, decay history, quarantines, and how trust changes route behavior.</p>
        </div>
        <span className="mono-chip">{demo.hubs.length} HUBS</span>
      </section>

      <section className="command-grid" aria-label="Trust Board modules">
        <TrustBoard hubs={demo.hubs} />
        <ImpactMetrics metrics={demo.impactMetrics} />
        <PacketFlowDecision routeDecision={demo.routeDecision} />
        <DigitalTwin
          activeRoute={demo.activeRoute}
          edges={demo.edges}
          hubs={demo.hubs}
          pulseHandshake={demo.pulseHandshake}
          selectedParcel={demo.parcel}
        />
      </section>
    </main>
  );
}
