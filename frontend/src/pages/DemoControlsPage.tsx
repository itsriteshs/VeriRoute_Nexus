import DemoControls from '../components/demo/DemoControls.tsx';
import DemoEventToast from '../components/demo/DemoEventToast.tsx';
import DemoTimeline from '../components/demo/DemoTimeline.tsx';
import EventLedger from '../components/ledger/EventLedger.tsx';
import AgentOpsMiniPanel from '../components/panels/AgentOpsMiniPanel.tsx';
import ColdChainMiniPanel from '../components/panels/ColdChainMiniPanel.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type DemoControlsPageProps = {
  demo: DemoState;
};

export default function DemoControlsPage({ demo }: DemoControlsPageProps) {
  return (
    <main className="dashboard">
      <DemoEventToast message={demo.toast} />
      <section className="page-header">
        <div>
          <p className="eyebrow">Operator Console / Local Demo</p>
          <h1>Demo Controls</h1>
          <p>Drive the judge sequence from one panel and watch local state update across every page.</p>
        </div>
        <span className="mono-chip">LOCAL STATE</span>
      </section>

      <section className="command-grid" aria-label="Demo control modules">
        <DemoControls
          acceptScan={demo.acceptScan}
          failHubB={demo.failHubB}
          injectFakeScan={demo.injectFakeScan}
          overloadHubB={demo.overloadHubB}
          raiseTemperature={demo.raiseTemperature}
          resetDemo={demo.resetDemo}
          triggerHandshake={demo.triggerHandshake}
        />
        <DemoTimeline alerts={demo.alerts} />
        <AgentOpsMiniPanel event={demo.agentOpsEvent} />
        <ColdChainMiniPanel state={demo.coldChainState} />
        <EventLedger events={demo.ledgerEvents} />
      </section>
    </main>
  );
}
