import type { ImmuneCheckResult } from '../../types/packetflow';

type ImmuneCheckTraceProps = {
  checks?: ImmuneCheckResult[];
};

export default function ImmuneCheckTrace({ checks = [] }: ImmuneCheckTraceProps) {
  if (checks.length === 0) {
    return <p className="trace-empty">No check trace attached yet.</p>;
  }

  return (
    <div className="immune-trace" aria-label="ImmuneNet check trace">
      {checks.map((check) => (
        <span className={`check-chip check-chip--${check.status.toLowerCase()}`} key={`${check.key}-${check.label}`}>
          <strong>{check.label}</strong>
          <em>{check.status}</em>
          {check.detail ? <small>{check.detail}</small> : null}
        </span>
      ))}
    </div>
  );
}
