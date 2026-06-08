type DemoControlsProps = {
  acceptScan: () => void;
  triggerHandshake: () => void;
  injectFakeScan: () => void;
  failHubB: () => void;
  overloadHubB: () => void;
  raiseTemperature: () => void;
  resetDemo: () => void;
  backendMode?: 'live' | 'mock';
};

const groups = [
  { title: 'Primary Flow', actions: ['acceptScan', 'triggerHandshake'] },
  { title: 'Disruption', actions: ['failHubB', 'overloadHubB'] },
  { title: 'ImmuneNet Attack', actions: ['injectFakeScan'] },
  { title: 'Cold Chain', actions: ['raiseTemperature'] },
  { title: 'Demo', actions: ['resetDemo'] },
] as const;

const actionLabels = {
  acceptScan: 'Accept Scan',
  triggerHandshake: 'Trigger ESP-NOW Handshake',
  failHubB: 'Fail HUB-B',
  overloadHubB: 'Overload HUB-B',
  injectFakeScan: 'Inject Fake Scan',
  raiseTemperature: 'Raise Temperature',
  resetDemo: 'Reset Demo',
};

export default function DemoControls(props: DemoControlsProps) {
  const isLive = props.backendMode === 'live';
  return (
    <section className="module-card demo-controls-panel">
      <div className="module-card__header">
        <div>
          <p>Operator Console</p>
          <h2>Demo Controls</h2>
        </div>
        <span className={`mono-chip ${isLive ? '' : 'mono-chip--warning'}`}>
          {isLive ? 'LIVE BACKEND' : 'LOCAL MOCK'}
        </span>
      </div>

      <div className="demo-control-groups">
        {groups.map((group) => (
          <div className="demo-control-group" key={group.title}>
            <p>{group.title}</p>
            <div>
              {group.actions.map((action) => (
                <button className={`demo-action demo-action--${action}`} key={action} onClick={props[action]} type="button">
                  {actionLabels[action]}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
