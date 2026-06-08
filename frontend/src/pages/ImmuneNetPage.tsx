import ImmuneNetAlerts from '../components/alerts/ImmuneNetAlerts.tsx';
import EventLedger from '../components/ledger/EventLedger.tsx';
import ImpactMetrics from '../components/metrics/ImpactMetrics.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type ImmuneNetPageProps = {
  demo: DemoState;
};

export default function ImmuneNetPage({ demo }: ImmuneNetPageProps) {
  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Immune Layer / Auditability</p>
          <h1>ImmuneNet</h1>
          <p>Inspect blocked claims, check traces, trust deltas, and local audit rows.</p>
        </div>
        <span className="mono-chip">{demo.alerts.length} ALERTS</span>
      </section>

      <section className="command-grid" aria-label="ImmuneNet modules">
        <ImmuneNetAlerts
          alerts={demo.alerts}
          onSelectAlert={demo.selectAlert}
          selectedAlert={demo.selectedAlert}
        />
        <ImpactMetrics metrics={demo.impactMetrics} />
        <EventLedger events={demo.ledgerEvents} />
      </section>
    </main>
  );
}
