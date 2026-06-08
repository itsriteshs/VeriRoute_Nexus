import type { GraphPoint } from '../types/packetflow';

export const twinLayout: Record<string, GraphPoint> = {
  'HUB-A': { x: 120, y: 210 },
  'HUB-B': { x: 330, y: 132 },
  'HUB-C': { x: 330, y: 296 },
  'COLD-HUB-C': { x: 560, y: 296 },
  'HUB-E': { x: 610, y: 132 },
  'CUSTOMER-ZONE': { x: 820, y: 210 },
};

export function getHubPosition(hubId: string): GraphPoint {
  return twinLayout[hubId] ?? { x: 0, y: 0 };
}

export function getParcelPosition(currentHub: string, nextHop: string): GraphPoint {
  const source = getHubPosition(currentHub);
  const target = getHubPosition(nextHop);

  return {
    x: source.x + (target.x - source.x) * 0.34,
    y: source.y + (target.y - source.y) * 0.34 - 24,
  };
}
