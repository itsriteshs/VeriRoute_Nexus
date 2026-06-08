import EventLedger from '../components/ledger/EventLedger.tsx';
import MovementProofPanel from '../components/panels/MovementProofPanel.tsx';
import PacketFlowDecision from '../components/panels/PacketFlowDecision.tsx';
import ParcelCard from '../components/panels/ParcelCard.tsx';
import type { DemoState } from '../hooks/useDemoState.ts';

type ParcelsPageProps = {
  demo: DemoState;
};

export default function ParcelsPage({ demo }: ParcelsPageProps) {
  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Parcel Evidence / MED-104</p>
          <h1>Parcels</h1>
          <p>Review the selected parcel, proof checks, route decision, and local movement ledger.</p>
        </div>
        <span className="mono-chip">{demo.parcel.status}</span>
      </section>

      <section className="command-grid" aria-label="Parcel proof modules">
        <ParcelCard parcel={demo.parcel} />
        <MovementProofPanel movementProof={demo.movementProof} />
        <PacketFlowDecision routeDecision={demo.routeDecision} />
        <EventLedger events={demo.ledgerEvents} />
      </section>
    </main>
  );
}
