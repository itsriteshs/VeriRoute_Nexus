const legendItems = [
  { label: 'Trusted', className: 'legend-dot--trusted' },
  { label: 'Risky', className: 'legend-dot--risky' },
  { label: 'Cold Hub', className: 'legend-dot--cold' },
  { label: 'Hardware Live', className: 'legend-dot--hardware' },
  { label: 'Active Route', className: 'legend-line--active' },
  { label: 'ESP-NOW Pulse', className: 'legend-dot--esp' },
];

export default function TwinLegend() {
  return (
    <div className="twin-legend" aria-label="Digital Twin legend">
      {legendItems.map((item) => (
        <span key={item.label}>
          <i className={item.className} />
          {item.label}
        </span>
      ))}
    </div>
  );
}
