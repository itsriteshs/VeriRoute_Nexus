import { useEffect, useState } from 'react';
import { apiGet } from '../api/client';
import { mapBackendLedgerEvents } from '../api/mappers';
import EventLedger from '../components/ledger/EventLedger';
import PacketFlowDecision from '../components/panels/PacketFlowDecision';
import ParcelCard from '../components/panels/ParcelCard';
import type { ActiveParcel, LedgerEvent, RouteDecision } from '../types/packetflow';

type ParcelDetailsProps = {
  parcelId?: string;
};

function mapParcel(raw: any, route: any): ActiveParcel {
  return {
    id: raw.id,
    type: raw.parcel_type,
    current_hub: raw.current_hub,
    previous_hub: raw.previous_hub,
    next_hop: route?.selected_next_hop || 'Pending',
    destination_hub: raw.destination_hub,
    priority: raw.priority,
    sla_minutes: raw.sla_minutes,
    sla_remaining_min: raw.sla_minutes,
    temperature_c: raw.current_temperature,
    temperature_limit_c: raw.temperature_limit,
    carrier_type: raw.carrier_type,
    status: raw.status,
    trust_state: raw.trust_state,
  };
}

function mapRoute(raw: any, parcelId: string): RouteDecision {
  return {
    parcel_id: parcelId,
    current_hub: raw?.current_hub || 'Pending',
    selected_next_hop: raw?.selected_next_hop || 'Pending',
    full_route: raw?.full_route || [],
    decision_type: 'Dynamic next-hop routing',
    triggered_by: 'Backend route history',
    reason: raw?.reason || 'No route decision recorded yet.',
    timestamp: raw?.created_at || 'Pending',
  };
}

export default function ParcelDetails({ parcelId }: ParcelDetailsProps) {
  const resolvedParcelId = parcelId || window.location.pathname.split('/').filter(Boolean)[1] || 'MED-104';
  const [parcel, setParcel] = useState<ActiveParcel | null>(null);
  const [route, setRoute] = useState<RouteDecision | null>(null);
  const [events, setEvents] = useState<LedgerEvent[]>([]);
  const [status, setStatus] = useState('Loading parcel...');

  async function loadParcel() {
    setStatus('Loading parcel...');
    try {
      const [parcelResponse, ledgerResponse] = await Promise.all([
        apiGet<{ parcel: any; latest_events: unknown[] }>(`/parcels/${resolvedParcelId}`),
        apiGet<{ events: unknown[]; latest_route?: any }>(`/ledger/parcel/${resolvedParcelId}`),
      ]);
      setRoute(mapRoute(ledgerResponse.latest_route, resolvedParcelId));
      setParcel(mapParcel(parcelResponse.parcel, ledgerResponse.latest_route));
      setEvents(mapBackendLedgerEvents(ledgerResponse.events || []));
      setStatus('Parcel loaded');
    } catch (error) {
      console.error(error);
      setStatus('Parcel load failed');
    }
  }

  useEffect(() => {
    loadParcel();
  }, [resolvedParcelId]);

  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">Parcel Evidence / {resolvedParcelId}</p>
          <h1>Parcel Details</h1>
          <p>Backend parcel state, latest PacketFlow route, and parcel-specific audit trail.</p>
        </div>
        <button className="demo-action" onClick={loadParcel} type="button">
          Refresh
        </button>
        <span className="mono-chip">{status}</span>
      </section>

      <section className="command-grid">
        {parcel ? <ParcelCard parcel={parcel} /> : <section className="module-card"><p>No parcel loaded.</p></section>}
        {route ? <PacketFlowDecision routeDecision={route} /> : null}
        <EventLedger events={events} />
      </section>
    </main>
  );
}
