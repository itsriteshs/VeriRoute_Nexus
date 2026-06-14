import type { GraphPoint } from '../types/packetflow';

export const twinLayout: Record<string, GraphPoint> = {
  'HUB-A': { x: 92, y: 218 },
  'HUB-B': { x: 365, y: 112 },
  'HUB-C': { x: 365, y: 334 },
  'COLD-HUB-C': { x: 635, y: 334 },
  'HUB-E': { x: 660, y: 112 },
  'CUSTOMER-ZONE': { x: 875, y: 218 },
};

export function getHubPosition(hubId: string): GraphPoint {
  return twinLayout[hubId] ?? { x: 0, y: 0 };
}

export function getParcelPosition(currentHub: string, nextHop: string): GraphPoint {
  const source = getHubPosition(currentHub);
  const target = getHubPosition(nextHop);
  const dx = target.x - source.x;
  const dy = target.y - source.y;
  const length = Math.hypot(dx, dy) || 1;
  const markerOffset = -28;

  return {
    x: source.x + dx * 0.5 + (-dy / length) * markerOffset,
    y: source.y + dy * 0.5 + (dx / length) * markerOffset,
  };
}
