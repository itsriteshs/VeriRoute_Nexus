import { useEffect, useState } from 'react';
import { apiGet } from '../api/client';
import { mapBackendLedgerEvents } from '../api/mappers';
import EventLedger from '../components/ledger/EventLedger';
import type { LedgerEvent } from '../types/packetflow';

export default function LedgerPage() {
  const [events, setEvents] = useState<LedgerEvent[]>([]);
  const [status, setStatus] = useState('Loading ledger...');

  async function loadLedger() {
    setStatus('Loading ledger...');
    try {
      const response = await apiGet<{ events: unknown[] }>('/ledger/events?limit=100');
      setEvents(mapBackendLedgerEvents(response.events || []));
      setStatus(`${response.events?.length || 0} events loaded`);
    } catch (error) {
      console.error(error);
      setStatus('Ledger load failed');
    }
  }

  useEffect(() => {
    loadLedger();
  }, []);

  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Audit Trail / Backend Ledger</p>
          <h1>Ledger</h1>
          <p>Inspect accepted, blocked, rerouted, hardware, trust, and scenario events from the backend.</p>
        </div>
        <button className="demo-action" onClick={loadLedger} type="button">
          Refresh
        </button>
        <span className="mono-chip">{status}</span>
      </section>

      <section className="command-grid">
        <EventLedger events={events} />
      </section>
    </main>
  );
}
