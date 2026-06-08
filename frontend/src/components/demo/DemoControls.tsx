import { useState } from 'react';

type DemoControlsProps = {
  acceptScan: () => void | Promise<void>;
  triggerHandshake: () => void | Promise<void>;
  injectFakeScan: () => void | Promise<void>;
  failHubB: () => void | Promise<void>;
  overloadHubB: () => void | Promise<void>;
  raiseTemperature: () => void | Promise<void>;
  resetDemo: () => void | Promise<void>;
  createMed104: () => void | Promise<void>;
  trafficJam: () => void | Promise<void>;
  weatherRisk: () => void | Promise<void>;
  cloneScan: () => void | Promise<void>;
  tamperEvent: () => void | Promise<void>;
  backendMode?: 'live' | 'mock';
};

const groups = [
  { title: 'Primary Flow', actions: ['createMed104', 'acceptScan', 'triggerHandshake'] },
  { title: 'Disruption', actions: ['failHubB', 'overloadHubB', 'trafficJam', 'weatherRisk'] },
  { title: 'ImmuneNet Attack', actions: ['injectFakeScan', 'cloneScan', 'tamperEvent'] },
  { title: 'Cold Chain', actions: ['raiseTemperature'] },
  { title: 'Demo', actions: ['resetDemo'] },
] as const;

const actionLabels = {
  createMed104: 'Create MED-104',
  acceptScan: 'Accept Scan',
  triggerHandshake: 'Trigger ESP-NOW Handshake',
  failHubB: 'Fail HUB-B',
  overloadHubB: 'Overload HUB-B',
  trafficJam: 'Traffic Jam',
  weatherRisk: 'Weather Risk',
  injectFakeScan: 'Inject Fake Scan',
  cloneScan: 'Clone Scan',
  tamperEvent: 'Tamper Event',
  raiseTemperature: 'Raise Temperature',
  resetDemo: 'Reset Demo',
};

type DemoAction = keyof typeof actionLabels;

export default function DemoControls(props: DemoControlsProps) {
  const isLive = props.backendMode === 'live';
  const [pendingAction, setPendingAction] = useState<DemoAction | null>(null);
  const [errorAction, setErrorAction] = useState<DemoAction | null>(null);

  async function runAction(action: DemoAction) {
    setPendingAction(action);
    setErrorAction(null);
    try {
      await props[action]();
    } catch (error) {
      console.error(error);
      setErrorAction(action);
    } finally {
      setPendingAction(null);
    }
  }

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
                <button
                  className={`demo-action demo-action--${action}`}
                  disabled={pendingAction !== null}
                  key={action}
                  onClick={() => runAction(action)}
                  type="button"
                >
                  {pendingAction === action ? 'Working...' : actionLabels[action]}
                </button>
              ))}
            </div>
            {errorAction && (group.actions as readonly DemoAction[]).includes(errorAction) ? (
              <span className="demo-control-error">Last action failed. Check backend status.</span>
            ) : null}
          </div>
        ))}
      </div>
    </section>
  );
}
