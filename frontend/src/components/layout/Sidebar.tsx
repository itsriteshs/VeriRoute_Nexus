import { Boxes, Gauge, Network, PlaySquare, Route, ShieldCheck } from 'lucide-react';
import { relayStatus, sidebarItems } from '../../data/mockData';
import StatusBadge from '../cards/StatusBadge';

const icons = [Gauge, Network, Boxes, ShieldCheck, Route, PlaySquare];

type SidebarProps = {
  currentPath: string;
  onNavigate: (path: string) => void;
};

export default function Sidebar({ currentPath, onNavigate }: SidebarProps) {
  return (
    <aside className="sidebar" aria-label="PacketFlow navigation">
      <div>
        <a
          className="sidebar__brand"
          href="/dashboard"
          onClick={(event) => {
            event.preventDefault();
            onNavigate('/dashboard');
          }}
        >
          <span className="sidebar__logo" aria-hidden="true">
            PF
          </span>
          <span>
            <strong>PacketFlow</strong>
            <small>ImmuneNet</small>
          </span>
        </a>

        <nav className="sidebar__nav" aria-label="Primary navigation">
          {sidebarItems.map((item, index) => {
            const Icon = icons[index];
            return (
              <a
                className={`sidebar__item ${currentPath === item.path ? 'is-active' : ''}`}
                href={item.path}
                key={item.path}
                onClick={(event) => {
                  event.preventDefault();
                  onNavigate(item.path);
                }}
              >
                <Icon size={18} strokeWidth={1.85} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>
      </div>

      <section className="relay-card">
        <div className="relay-card__signal" aria-hidden="true" />
        <p>{relayStatus.title}</p>
        <strong>{relayStatus.route}</strong>
        <StatusBadge label={relayStatus.status} tone="warning" />
        <div className="relay-card__wave" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
      </section>
    </aside>
  );
}
