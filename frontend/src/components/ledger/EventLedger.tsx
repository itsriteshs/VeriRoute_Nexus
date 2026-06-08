import { useMemo, useState } from 'react';
import type { LedgerEvent } from '../../types/packetflow';
import LedgerFilters, { type LedgerFilter } from './LedgerFilters.tsx';
import LedgerRow from './LedgerRow.tsx';

type EventLedgerProps = {
  events: LedgerEvent[];
};

export default function EventLedger({ events }: EventLedgerProps) {
  const [activeFilter, setActiveFilter] = useState<LedgerFilter>('all');
  const filteredEvents = useMemo(
    () => events.filter((event) => activeFilter === 'all' || event.category === activeFilter),
    [activeFilter, events],
  );

  return (
    <section className="module-card event-ledger">
      <div className="module-card__header">
        <div>
          <p>Audit Ledger</p>
          <h2>Event Ledger</h2>
        </div>
        <span className="mono-chip">{filteredEvents.length} ROWS</span>
      </div>

      <LedgerFilters activeFilter={activeFilter} onChange={setActiveFilter} />

      <div className="ledger-table" role="table" aria-label="PacketFlow audit ledger">
        <div className="ledger-row ledger-row--head" role="row">
          <span>Time</span>
          <span>Parcel</span>
          <span>Hub</span>
          <span>Event</span>
          <span>Geofence</span>
          <span>Speed</span>
          <span>Route graph</span>
          <span>Clone</span>
          <span>Cold-chain</span>
          <span>Tamper</span>
          <span>Decision</span>
          <span>Action</span>
          <span>Reason</span>
        </div>
        {filteredEvents.length === 0 ? (
          <p className="ledger-empty">Run demo controls to write local audit rows.</p>
        ) : (
          filteredEvents.map((event) => <LedgerRow event={event} key={event.id} />)
        )}
      </div>
    </section>
  );
}
