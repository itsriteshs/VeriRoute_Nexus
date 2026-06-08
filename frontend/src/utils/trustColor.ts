import type { Hub } from '../types/packetflow';

export type TrustColor = {
  fill: string;
  stroke: string;
  label: string;
};

export function getHubTrustColor(hub: Hub): TrustColor {
  if (hub.status === 'failed') {
    return { fill: '#E2E7E1', stroke: '#DC4A45', label: 'Failed' };
  }

  if (hub.trust_status === 'quarantined') {
    return { fill: '#F6D8D7', stroke: '#DC4A45', label: 'Quarantined' };
  }

  if (hub.trust_status === 'risky') {
    return { fill: '#F1C68C', stroke: '#DC4A45', label: 'Risky' };
  }

  if (hub.trust_status === 'watch') {
    return { fill: '#F3D989', stroke: '#C8A43D', label: 'Watch' };
  }

  if (hub.cold_chain) {
    return { fill: '#CDE4DF', stroke: '#82A89C', label: 'Cold Hub' };
  }

  return { fill: '#B1E09D', stroke: '#2F8F5B', label: 'Trusted' };
}
