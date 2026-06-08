import type { ColdChainState } from '../../types/packetflow';
import { formatTemperature } from '../../utils/formatters.ts';

type ColdChainMiniPanelProps = {
  state: ColdChainState;
};

export default function ColdChainMiniPanel({ state }: ColdChainMiniPanelProps) {
  return (
    <section className="module-card mini-panel coldchain-panel">
      <div className="module-card__header">
        <div>
          <p>Cold Chain</p>
          <h2>Temperature Route</h2>
        </div>
        <span className={`mono-chip ${state ? 'mono-chip--warning' : ''}`}>{state ? 'RISK' : 'CLEAR'}</span>
      </div>
      {state ? (
        <div className="mini-panel__body">
          <strong>
            {formatTemperature(state.current_temperature_c)} / {formatTemperature(state.limit_c)}
          </strong>
          <p>{state.status}</p>
          <span>{state.action}</span>
        </div>
      ) : (
        <p className="mini-panel__empty">Temperature is within medicine SLA limit.</p>
      )}
    </section>
  );
}
