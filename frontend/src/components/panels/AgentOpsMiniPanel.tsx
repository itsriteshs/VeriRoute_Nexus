import type { AgentOpsEvent } from '../../types/packetflow';

type AgentOpsMiniPanelProps = {
  event: AgentOpsEvent;
};

export default function AgentOpsMiniPanel({ event }: AgentOpsMiniPanelProps) {
  return (
    <section className="module-card mini-panel agentops-panel">
      <div className="module-card__header">
        <div>
          <p>AgentOps</p>
          <h2>Reroute Trace</h2>
        </div>
        <span className="mono-chip">{event ? 'ACTIVE' : 'STANDBY'}</span>
      </div>
      {event ? (
        <div className="mini-panel__body">
          <strong>{event.title}</strong>
          <p>{event.detail}</p>
          <span>{event.timestamp}</span>
        </div>
      ) : (
        <p className="mini-panel__empty">Awaiting disruption event.</p>
      )}
    </section>
  );
}
