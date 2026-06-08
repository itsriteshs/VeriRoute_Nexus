// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: Main header bar with search field, live status indicators, and manual sync controls.

import { Search, RefreshCw } from 'lucide-react';
import StatusBadge from '../cards/StatusBadge';

type TopBarProps = {
  demo?: any;
};

export default function TopBar({ demo }: TopBarProps) {
  const backendMode = demo?.backendMode || 'mock';
  const websocketStatus = demo?.websocketStatus || 'disconnected';
  const lastEvent = demo?.lastEvent || 'None';

  const isHardwareEvent =
    lastEvent.includes('hardware') ||
    lastEvent.includes('p2p') ||
    lastEvent.includes('ble') ||
    lastEvent.includes('esp_now');
  const hardwareLabel = isHardwareEvent ? 'Hardware: Event Received' : 'Hardware: Standby';
  const hardwareTone = isHardwareEvent ? 'primary' : 'muted';

  return (
    <header className="topbar">
      <label className="search-field">
        <Search size={18} strokeWidth={1.8} />
        <input placeholder="Search parcel, hub, event…" type="search" />
      </label>

      <div className="topbar__right">
        <div className="topbar__badges">
          <StatusBadge
            label={backendMode === 'live' ? 'Backend: Live' : 'Backend: Mock'}
            tone={backendMode === 'live' ? 'primary' : 'warning'}
          />
          <StatusBadge
            label={
              websocketStatus === 'connected'
                ? 'WebSocket: Connected'
                : websocketStatus === 'connecting'
                ? 'WebSocket: Reconnecting'
                : websocketStatus === 'error'
                ? 'WebSocket: Error'
                : 'WebSocket: Offline'
            }
            tone={
              websocketStatus === 'connected'
                ? 'primary'
                : websocketStatus === 'connecting'
                ? 'warning'
                : 'muted'
            }
          />
          <StatusBadge label={hardwareLabel} tone={hardwareTone} />
        </div>
        {demo?.syncBackend && (
          <button
            className="sync-button"
            onClick={() => demo.syncBackend()}
            title="Sync Backend State"
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--color-muted)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '11px',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
            type="button"
          >
            <RefreshCw size={13} className={websocketStatus === 'connecting' ? 'spin' : ''} />
            Sync
          </button>
        )}
        <span className="topbar__sync" style={{ fontSize: '11px', color: 'var(--color-muted)' }}>
          EVENT: {lastEvent.toUpperCase()}
        </span>
        <span className="team-pill">
          <i aria-hidden="true" />
          Team Aristotle
        </span>
      </div>
    </header>
  );
}
