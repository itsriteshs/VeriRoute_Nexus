import type { Edge } from '../../types/packetflow';
import { getHubPosition } from '../../utils/graphLayout.ts';

type TwinEdgeProps = {
  edge: Edge;
  pulseHandshake?: boolean;
};

export default function TwinEdge({ edge, pulseHandshake = false }: TwinEdgeProps) {
  const source = getHubPosition(edge.source);
  const target = getHubPosition(edge.target);
  const midX = (source.x + target.x) / 2;
  const midY = (source.y + target.y) / 2;
  const className = [
    'twin-edge',
    edge.active ? 'twin-edge--active' : '',
    edge.espNow ? 'twin-edge--esp' : '',
    edge.espNow && pulseHandshake ? 'twin-edge--pulse-now' : '',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <g className={className}>
      <line x1={source.x} x2={target.x} y1={source.y} y2={target.y} />
      {edge.espNow ? (
        <>
          <circle className="twin-edge__pulse" cx={midX} cy={midY} r="8" />
          <text className="twin-edge__label" x={midX} y={midY - 18}>
            ESP-NOW handshake
          </text>
        </>
      ) : null}
    </g>
  );
}
