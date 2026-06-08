import type { DemoAlertType } from '../../types/packetflow';

export type LedgerFilter = 'all' | DemoAlertType;

type LedgerFiltersProps = {
  activeFilter: LedgerFilter;
  onChange: (filter: LedgerFilter) => void;
};

const filters: Array<{ label: string; value: LedgerFilter }> = [
  { label: 'All', value: 'all' },
  { label: 'Accepted', value: 'accepted' },
  { label: 'Blocked', value: 'blocked' },
  { label: 'Rerouted', value: 'rerouted' },
  { label: 'Cold-chain', value: 'cold_chain' },
  { label: 'Trust', value: 'trust_update' },
  { label: 'P2P', value: 'p2p' },
];

export default function LedgerFilters({ activeFilter, onChange }: LedgerFiltersProps) {
  return (
    <div className="ledger-filters" aria-label="Ledger filters">
      {filters.map((filter) => (
        <button
          className={activeFilter === filter.value ? 'is-active' : ''}
          key={filter.value}
          onClick={() => onChange(filter.value)}
          type="button"
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
