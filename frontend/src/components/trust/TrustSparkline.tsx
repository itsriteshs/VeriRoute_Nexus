type TrustSparklineProps = {
  values?: number[];
};

export default function TrustSparkline({ values = [] }: TrustSparklineProps) {
  const points = values.length > 0 ? values : [0.8, 0.8, 0.8];
  const path = points
    .map((value, index) => {
      const x = (index / Math.max(points.length - 1, 1)) * 90 + 5;
      const y = 36 - value * 30;
      return `${index === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
    })
    .join(' ');

  return (
    <svg className="trust-sparkline" role="img" viewBox="0 0 100 42" aria-label="Trust score history">
      <path d={path} />
      {points.map((value, index) => {
        const x = (index / Math.max(points.length - 1, 1)) * 90 + 5;
        const y = 36 - value * 30;
        return <circle cx={x} cy={y} key={`${value}-${index}`} r="2.8" />;
      })}
    </svg>
  );
}
