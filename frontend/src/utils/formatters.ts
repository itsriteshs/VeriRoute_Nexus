export function formatTemperature(value: number) {
  return `${value.toFixed(1)}°C`;
}

export function formatScore(value: number) {
  return value.toFixed(2);
}

export function formatRiskPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export function formatBoolean(value: boolean) {
  return value ? 'Verified' : 'Not verified';
}
