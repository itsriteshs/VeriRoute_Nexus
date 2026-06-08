import type { PanelPreview } from '../../types/packetflow';
import StatusBadge from './StatusBadge';

type PanelProps = {
  panel: PanelPreview;
};

export default function Panel({ panel }: PanelProps) {
  return (
    <section
      className={[
        'panel-card',
        panel.variant === 'dark' ? 'panel-card--dark' : '',
        panel.variant === 'wide' ? 'panel-card--wide' : '',
      ]
        .filter(Boolean)
        .join(' ')}
    >
      <div className="panel-card__header">
        <p>{panel.eyebrow}</p>
        <StatusBadge label={panel.meta} tone={panel.tone} />
      </div>
      <div>
        <h2>{panel.title}</h2>
        <p className="panel-card__description">{panel.description}</p>
      </div>
      <div className="panel-card__preview" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>
    </section>
  );
}
