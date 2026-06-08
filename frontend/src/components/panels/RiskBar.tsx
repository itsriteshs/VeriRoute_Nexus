import { formatRiskPercent, formatScore } from '../../utils/formatters.ts';

type RiskBarProps = {
  label: string;
  value: number;
  weight: number;
  status?: string;
};

export default function RiskBar({ label, value, weight, status }: RiskBarProps) {
  const weighted = value * weight;

  return (
    <div className="risk-bar">
      <div className="risk-bar__top">
        <span>{label}</span>
        <strong>{formatRiskPercent(value)}</strong>
      </div>
      <div className="risk-bar__track">
        <i style={{ width: formatRiskPercent(value) }} />
      </div>
      <div className="risk-bar__meta">
        <span>Weight {formatScore(weight)}</span>
        <span>Weighted {formatScore(weighted)}</span>
        {status ? <em>{status}</em> : null}
      </div>
    </div>
  );
}
