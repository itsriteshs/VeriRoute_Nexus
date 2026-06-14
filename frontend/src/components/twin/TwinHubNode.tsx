import type { Hub } from '../../types/packetflow';
import { getHubPosition } from '../../utils/graphLayout.ts';
import { getHubTrustColor } from '../../utils/trustColor.ts';

type TwinHubNodeProps = {
  hub: Hub;
  selected: boolean;
  onSelect: (hub: Hub) => void;
  routeRole: string;
  routeStep: number;
};

export default function TwinHubNode({ hub, selected, onSelect, routeRole, routeStep }: TwinHubNodeProps) {
  const position = getHubPosition(hub.id);
  const colors = getHubTrustColor(hub);
  const isRouteHub = routeStep > 0;

  return (
    <g
      className={[
        'twin-hub',
        selected ? 'twin-hub--selected' : '',
        isRouteHub ? 'twin-hub--route' : '',
        hub.status === 'overloaded' ? 'twin-hub--overloaded' : '',
        hub.status === 'failed' ? 'twin-hub--failed' : '',
      ]
        .filter(Boolean)
        .join(' ')}
      onClick={() => onSelect(hub)}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          onSelect(hub);
        }
      }}
      role="button"
      tabIndex={0}
      transform={`translate(${position.x} ${position.y})`}
    >
      {isRouteHub ? (
        <>
          <circle className="twin-hub__step-ring" cx="-50" cy="-39" r="15" />
          <text className="twin-hub__step" textAnchor="middle" x="-50" y="-34">
            {routeStep}
          </text>
        </>
      ) : null}
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
      <text className="twin-hub__role" textAnchor="middle" y="34">
        {routeRole}
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
