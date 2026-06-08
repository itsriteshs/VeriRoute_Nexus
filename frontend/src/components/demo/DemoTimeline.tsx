import type { DemoAlert } from '../../types/packetflow';

type DemoTimelineProps = {
  alerts: DemoAlert[];
};

export default function DemoTimeline({ alerts }: DemoTimelineProps) {
  return (
    <section className="module-card demo-timeline">
      <div className="module-card__header">
        <div>
          <p>Demo Timeline</p>
          <h2>Local Events</h2>
        </div>
        <span className="mono-chip">{alerts.length} EVENTS</span>
      </div>
      <div className="demo-timeline__list">
        {alerts.length === 0 ? (
          <p className="demo-timeline__empty">Run a demo action to create local events.</p>
        ) : (
          alerts.slice(0, 4).map((alert) => (
            <article key={alert.id}>
              <span>{alert.status}</span>
              <strong>{alert.title}</strong>
              <small>{alert.timestamp}</small>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
