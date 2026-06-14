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

function getTwinMode(parcel: ActiveParcel, activeRoute: string[]) {
  const temperatureRisk = parcel.temperature_c > parcel.temperature_limit_c;
  const coldRoute = activeRoute.some((hubId) => hubId.includes('COLD'));
  const delivered = parcel.current_hub === parcel.destination_hub || parcel.status.toLowerCase().includes('delivered');

  if (delivered) {
    return {
      label: 'Delivered',
      tone: 'success',
      title: 'Customer zone verified',
      detail: `${parcel.id} has reached ${parcel.destination_hub}.`,
    };
  }

  if (temperatureRisk || coldRoute) {
    return {
      label: 'Cold-chain reroute',
      tone: 'warning',
      title: 'Temperature risk detected',
      detail: `${parcel.id} is above ${parcel.temperature_limit_c}C, so PacketFlow is favoring the cold corridor.`,
    };
  }

  return {
    label: 'Trusted movement',
    tone: 'success',
    title: 'Next hop is pre-authorised',
    detail: `${parcel.current_hub} is handing ${parcel.id} to ${parcel.next_hop} after identity, GPS, route, and temperature checks.`,
  };
}

function getHubRouteRole(hubId: string, parcel: ActiveParcel, activeRoute: string[]) {
  const routeIndex = activeRoute.indexOf(hubId);

  if (hubId === parcel.current_hub) return 'Current scan';
  if (hubId === parcel.next_hop) return 'Next hop';
  if (hubId === parcel.destination_hub) return 'Destination';
  if (routeIndex >= 0) return `Step ${routeIndex + 1}`;
  return 'Standby';
}

export default function DigitalTwin({ hubs, edges, activeRoute, selectedParcel, pulseHandshake = false }: DigitalTwinProps) {
  const defaultHub = useMemo(() => hubs.find((hub) => hub.id === 'HUB-A') ?? hubs[0], [hubs]);
  const [selectedHub, setSelectedHub] = useState<Hub>(defaultHub);
  const selectedHubFromState = hubs.find((hub) => hub.id === selectedHub.id) ?? defaultHub;
  const mode = getTwinMode(selectedParcel, activeRoute);
  const currentRouteIndex = Math.max(0, activeRoute.indexOf(selectedParcel.current_hub));
  const totalSteps = Math.max(activeRoute.length - 1, 1);
  const routeProgress = Math.min(100, Math.max(12, ((currentRouteIndex + 0.42) / totalSteps) * 100));
  const highTrustHubs = hubs.filter((hub) => hub.trust_score >= 0.8 && hub.status !== 'failed').length;
  const activeEdgeCount = edges.filter((edge) => isActiveRouteEdge(edge, activeRoute)).length;

  return (
    <section className="module-card module-card--twin digital-twin-card">
      <div className="module-card__header digital-twin-card__header">
        <div>
          <p>Network Simulation</p>
          <h2>Digital Twin</h2>
        </div>
        <span className={`simulation-pill simulation-pill--${mode.tone}`}>{mode.label}</span>
      </div>

      <div className="simulation-brief" aria-label="Simulation status summary">
        <div>
          <span>What is happening now</span>
          <strong>{mode.title}</strong>
          <p>{mode.detail}</p>
        </div>
        <div className="simulation-brief__metrics">
          <span>
            <strong>{selectedParcel.current_hub}</strong>
            Current hub
          </span>
          <span>
            <strong>{selectedParcel.next_hop}</strong>
            Next hop
          </span>
          <span>
            <strong>{highTrustHubs}/{hubs.length}</strong>
            Trusted hubs
          </span>
        </div>
      </div>

      <div className="route-progress" aria-label="Active route progress">
        <div className="route-progress__track">
          <i style={{ width: `${routeProgress}%` }} />
        </div>
        <div className="route-progress__hops">
          {activeRoute.map((hubId, index) => (
            <button
              className={[
                hubId === selectedParcel.current_hub ? 'is-current' : '',
                hubId === selectedParcel.next_hop ? 'is-next' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              key={`${hubId}-${index}`}
              onClick={() => {
                const routeHub = hubs.find((hub) => hub.id === hubId);
                if (routeHub) setSelectedHub(routeHub);
              }}
              type="button"
            >
              <span>{index + 1}</span>
              {hubId}
            </button>
          ))}
        </div>
      </div>

      <div className="digital-twin-shell">
        <div className="digital-twin-stage">
          <div className="digital-twin-stage__toolbar">
            <span>{activeEdgeCount} live route links</span>
            <span>{selectedParcel.carrier_type} carrier</span>
            <span>{selectedParcel.temperature_c.toFixed(1)}C / limit {selectedParcel.temperature_limit_c}C</span>
          </div>
          <svg aria-label="PacketFlow Digital Twin graph" className="digital-twin-svg" viewBox="0 0 940 430">
            <defs>
              <filter id="nodeShadow" x="-20%" y="-30%" width="140%" height="160%">
                <feDropShadow dx="0" dy="12" floodColor="#061C15" floodOpacity="0.12" stdDeviation="12" />
              </filter>
              <marker id="routeArrow" markerHeight="10" markerWidth="10" orient="auto" refX="7" refY="3" viewBox="0 0 10 6">
                <path d="M0 0 L8 3 L0 6 Z" fill="#2f8f5b" />
              </marker>
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
              <TwinHubNode
                hub={hub}
                key={hub.id}
                onSelect={setSelectedHub}
                routeRole={getHubRouteRole(hub.id, selectedParcel, activeRoute)}
                routeStep={activeRoute.indexOf(hub.id) + 1}
                selected={selectedHubFromState.id === hub.id}
              />
            ))}
          </svg>
          <TwinLegend />
        </div>
        <HubDetailPopover activeRoute={activeRoute} hub={selectedHubFromState} parcel={selectedParcel} />
      </div>
    </section>
  );
}
