import type { Hub } from '../../types/packetflow';
import { getHubPosition } from '../../utils/graphLayout.ts';
import { getHubTrustColor } from '../../utils/trustColor.ts';

type TwinHubNodeProps = {
  hub: Hub;
  selected: boolean;
  onSelect: (hub: Hub) => void;
};

export default function TwinHubNode({ hub, selected, onSelect }: TwinHubNodeProps) {
  const position = getHubPosition(hub.id);
  const colors = getHubTrustColor(hub);

  return (
    <g
      className={[
        'twin-hub',
        selected ? 'twin-hub--selected' : '',
        hub.status === 'overloaded' ? 'twin-hub--overloaded' : '',
        hub.status === 'failed' ? 'twin-hub--failed' : '',
      ]
        .filter(Boolean)
        .join(' ')}
      onClick={() => onSelect(hub)}
      role="button"
      tabIndex={0}
      transform={`translate(${position.x} ${position.y})`}
    >
      <rect
        className="twin-hub__body"
        fill={colors.fill}
        height="74"
        rx="24"
        stroke={colors.stroke}
        width="112"
        x="-56"
        y="-37"
      />
      <text className="twin-hub__id" textAnchor="middle" y="-5">
        {hub.id}
      </text>
      <text className="twin-hub__score" textAnchor="middle" y="18">
        {hub.trust_score.toFixed(2)}
      </text>
      {hub.cold_chain ? (
        <text className="twin-hub__cold" textAnchor="middle" y="47">
          COLD
        </text>
      ) : null}
      {hub.hardware_live ? (
        <>
          <circle className="twin-hub__hardware-glow" cx="48" cy="-30" r="12" />
          <circle className="twin-hub__hardware-dot" cx="48" cy="-30" r="5" />
        </>
      ) : null}
    </g>
  );
}
