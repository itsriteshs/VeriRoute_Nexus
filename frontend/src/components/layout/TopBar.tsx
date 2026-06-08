import { Search } from 'lucide-react';
import { topBarBadges } from '../../data/mockData';
import StatusBadge from '../cards/StatusBadge';

export default function TopBar() {
  return (
    <header className="topbar">
      <label className="search-field">
        <Search size={18} strokeWidth={1.8} />
        <input placeholder="Search parcel, hub, event…" type="search" />
      </label>

      <div className="topbar__right">
        <div className="topbar__badges">
          {topBarBadges.map((badge) => (
            <StatusBadge key={badge.label} label={badge.label} tone={badge.tone} />
          ))}
        </div>
        <span className="team-pill">Team Aristotle</span>
      </div>
    </header>
  );
}
