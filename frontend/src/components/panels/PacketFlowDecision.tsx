import type { RouteDecision } from '../../types/packetflow';
import RoutePath from './RoutePath';

type PacketFlowDecisionProps = {
  routeDecision: RouteDecision;
};

export default function PacketFlowDecision({ routeDecision }: PacketFlowDecisionProps) {
  return (
    <section className="module-card demo-panel decision-panel">
      <div className="module-card__header">
        <div>
          <p>PacketFlow Engine</p>
          <h2>PacketFlow Decision</h2>
        </div>
        <span className="mono-chip mono-chip--light">NEXT HOP: {routeDecision.selected_next_hop}</span>
      </div>

      <div className="decision-panel__hero">
        <span>Selected next hop</span>
        <strong>{routeDecision.selected_next_hop}</strong>
      </div>

      <RoutePath route={routeDecision.full_route} selectedHop={routeDecision.selected_next_hop} />

      <p className="module-card__copy">{routeDecision.reason}</p>

      <dl className="decision-panel__meta">
        <div>
          <dt>Decision type</dt>
          <dd>{routeDecision.decision_type}</dd>
        </div>
        <div>
          <dt>Triggered by</dt>
          <dd>{routeDecision.triggered_by}</dd>
        </div>
        <div>
          <dt>Timestamp</dt>
          <dd>{routeDecision.timestamp}</dd>
        </div>
      </dl>
    </section>
  );
}
