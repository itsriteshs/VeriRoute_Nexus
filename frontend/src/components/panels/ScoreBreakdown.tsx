import type { CandidateScore, RiskFactor } from '../../types/packetflow';
import { formatScore } from '../../utils/formatters.ts';
import RiskBar from './RiskBar';

type ScoreBreakdownProps = {
  candidateScores: CandidateScore[];
};

export default function ScoreBreakdown({ candidateScores }: ScoreBreakdownProps) {
  const selectedCandidate = candidateScores.find((candidate) => candidate.selected) ?? candidateScores[0];
  const selectedRiskFactors: RiskFactor[] = [
    { key: 'sla_risk', label: 'SLA risk', value: selectedCandidate.sla_risk, weight: 0.3, status: 'SLA safe' },
    {
      key: 'congestion_risk',
      label: 'Congestion',
      value: selectedCandidate.congestion_risk,
      weight: 0.25,
      status: 'Manageable',
    },
    { key: 'trust_risk', label: 'Trust risk', value: selectedCandidate.trust_risk, weight: 0.2, status: 'Low risk' },
    {
      key: 'condition_risk',
      label: 'Condition',
      value: selectedCandidate.condition_risk,
      weight: 0.15,
      status: 'Temperature OK',
    },
    { key: 'cost_score', label: 'Cost', value: selectedCandidate.cost_score, weight: 0.1, status: 'Efficient' },
  ];

  return (
    <section className="module-card demo-panel score-panel">
      <div className="module-card__header">
        <div>
          <p>Risk Formula</p>
          <h2>Score Breakdown</h2>
        </div>
        <span className="mono-chip">HUB-B SELECTED</span>
      </div>

      <p className="score-panel__formula">
        Score = 0.30×SLA + 0.25×Congestion + 0.20×Trust + 0.15×Condition + 0.10×Cost
      </p>

      <div className="risk-bar-grid">
        {selectedRiskFactors.map((factor) => (
          <RiskBar
            key={factor.key}
            label={factor.label}
            status={factor.status}
            value={factor.value}
            weight={factor.weight}
          />
        ))}
      </div>

      <div className="candidate-table" role="table" aria-label="Candidate route comparison">
        <div className="candidate-table__row candidate-table__row--head" role="row">
          <span>Candidate</span>
          <span>SLA</span>
          <span>Cong.</span>
          <span>Trust</span>
          <span>Cond.</span>
          <span>Final</span>
          <span>Result</span>
        </div>
        {candidateScores.map((candidate) => (
          <div className={`candidate-table__row ${candidate.selected ? 'is-selected' : ''}`} key={candidate.hub_id} role="row">
            <span>{candidate.hub_id}</span>
            <span>{formatScore(candidate.sla_risk)}</span>
            <span>{formatScore(candidate.congestion_risk)}</span>
            <span>{formatScore(candidate.trust_risk)}</span>
            <span>{formatScore(candidate.condition_risk)}</span>
            <span>{formatScore(candidate.final_score)}</span>
            <strong>{candidate.result}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
