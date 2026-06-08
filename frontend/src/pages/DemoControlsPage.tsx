import DemoControls from '../components/demo/DemoControls.tsx';
import DemoEventToast from '../components/demo/DemoEventToast.tsx';
import DemoTimeline from '../components/demo/DemoTimeline.tsx';
import EventLedger from '../components/ledger/EventLedger.tsx';
import AgentOpsMiniPanel from '../components/panels/AgentOpsMiniPanel.tsx';
import ColdChainMiniPanel from '../components/panels/ColdChainMiniPanel.tsx';
import type { LiveDemoState } from '../hooks/usePacketFlowLiveState.ts';

type DemoControlsPageProps = {
  demo: LiveDemoState;
};

export default function DemoControlsPage({ demo }: DemoControlsPageProps) {
  const isLive = demo.backendMode === 'live';
  return (
    <main className="dashboard">
      <DemoEventToast message={demo.toast} />
      <section className="page-header">
        <div>
          <p className="eyebrow">Operator Console / Local Demo</p>
          <h1>Demo Controls</h1>
          <p>Drive the judge sequence from one panel and watch local state update across every page.</p>
        </div>
        <span className={`mono-chip ${isLive ? '' : 'mono-chip--warning'}`}>
          {isLive ? 'LIVE BACKEND' : 'LOCAL MOCK'}
        </span>
      </section>

      <section className="command-grid" aria-label="Demo control modules">
        <DemoControls
          acceptScan={demo.acceptScan}
          cloneScan={demo.cloneScan}
          createMed104={demo.createMed104}
          failHubB={demo.failHubB}
          injectFakeScan={demo.injectFakeScan}
          overloadHubB={demo.overloadHubB}
          raiseTemperature={demo.raiseTemperature}
          resetDemo={demo.resetDemo}
          tamperEvent={demo.tamperEvent}
          trafficJam={demo.trafficJam}
          triggerHandshake={demo.triggerHandshake}
          weatherRisk={demo.weatherRisk}
          backendMode={demo.backendMode}
        />
        <DemoTimeline alerts={demo.alerts} />
        <AgentOpsMiniPanel event={demo.agentOpsEvent} />
        <ColdChainMiniPanel state={demo.coldChainState} />
        <EventLedger events={demo.ledgerEvents} />
      </section>
    </main>
  );
}
