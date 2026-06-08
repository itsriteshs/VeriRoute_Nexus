import { useMemo, useState } from 'react';
import type { ActiveParcel, Edge, Hub } from '../../types/packetflow';
import HubDetailPopover from './HubDetailPopover';
import ParcelMarker from './ParcelMarker';
import TwinEdge from './TwinEdge';
import TwinHubNode from './TwinHubNode';
import TwinLegend from './TwinLegend';

type DigitalTwinProps = {
  hubs: Hub[];
  edges: Edge[];
  activeRoute: string[];
  selectedParcel: ActiveParcel;
  pulseHandshake?: boolean;
};

function isActiveRouteEdge(edge: Edge, activeRoute: string[]) {
  return activeRoute.some((hubId, index) => hubId === edge.source && activeRoute[index + 1] === edge.target);
}

export default function DigitalTwin({ hubs, edges, activeRoute, selectedParcel, pulseHandshake = false }: DigitalTwinProps) {
  const defaultHub = useMemo(() => hubs.find((hub) => hub.id === 'HUB-A') ?? hubs[0], [hubs]);
  const [selectedHub, setSelectedHub] = useState<Hub>(defaultHub);
  const selectedHubFromState = hubs.find((hub) => hub.id === selectedHub.id) ?? defaultHub;

  return (
    <section className="module-card module-card--twin digital-twin-card">
      <div className="module-card__header">
        <div>
          <p>Network Canvas</p>
          <h2>Digital Twin</h2>
        </div>
        <span className="mono-chip">{selectedParcel.id} / ACTIVE ROUTE</span>
      </div>

      <div className="digital-twin-shell">
        <div className="digital-twin-stage">
          <svg aria-label="PacketFlow Digital Twin graph" className="digital-twin-svg" viewBox="0 0 940 430">
            <defs>
              <filter id="nodeShadow" x="-20%" y="-30%" width="140%" height="160%">
                <feDropShadow dx="0" dy="12" floodColor="#061C15" floodOpacity="0.12" stdDeviation="12" />
              </filter>
            </defs>
            <rect className="digital-twin-svg__surface" height="430" rx="36" width="940" />
            {edges.map((edge) => (
              <TwinEdge
                edge={{ ...edge, active: isActiveRouteEdge(edge, activeRoute) }}
                key={edge.id}
                pulseHandshake={pulseHandshake}
              />
            ))}
            <ParcelMarker parcel={selectedParcel} />
            {hubs.map((hub) => (
              <TwinHubNode hub={hub} key={hub.id} onSelect={setSelectedHub} selected={selectedHubFromState.id === hub.id} />
            ))}
          </svg>
          <TwinLegend />
        </div>
        <HubDetailPopover hub={selectedHubFromState} />
      </div>
    </section>
  );
}
