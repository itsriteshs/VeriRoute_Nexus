import { useMemo, useState } from 'react';
import { apiPost } from '../api/client';
import { endpoints } from '../api/endpoints';

type ScanResult = {
  decision: string;
  action: string;
  led: string;
  reason: string;
  failed_checks?: string[];
};

type ScanPageProps = {
  hubId?: string;
};

const validGps = { lat: 11.0168, lng: 76.9558, accuracy_m: 18 };
const fakeGps = { lat: 11.1, lng: 77.1, accuracy_m: 20 };

export default function ScanPage({ hubId }: ScanPageProps) {
  const resolvedHubId = hubId || window.location.pathname.split('/').filter(Boolean)[1] || 'HUB-A';
  const parcelId = useMemo(() => new URLSearchParams(window.location.search).get('parcel_id') || 'MED-104', []);
  const [gps, setGps] = useState(validGps);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [status, setStatus] = useState('Ready for scan');
  const [isLoading, setIsLoading] = useState(false);

  function captureBrowserGps() {
    setStatus('Requesting browser GPS...');
    if (!navigator.geolocation) {
      setStatus('Browser GPS unavailable. Use fallback coordinates.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setGps({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
          accuracy_m: position.coords.accuracy,
        });
        setStatus('Browser GPS captured.');
      },
      () => setStatus('GPS permission failed. Use fallback coordinates.'),
      { enableHighAccuracy: true, timeout: 8000 },
    );
  }

  async function submitScan() {
    setIsLoading(true);
    setStatus('Submitting proof-of-movement...');
    try {
      const response = await apiPost<ScanResult>(endpoints.scan, {
        parcel_id: parcelId,
        hub_id: resolvedHubId,
        scanner_id: `PHONE-${resolvedHubId}`,
        rfid_verified: true,
        qr_verified: true,
        gps,
        temperature_c: 24.3,
        carrier_type: 'van',
        tamper: false,
      });
      setResult(response);
      setStatus('Scan decision received.');
    } catch (error) {
      console.error(error);
      setStatus('Scan failed. Check backend and payload.');
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="dashboard">
      <section className="page-header">
        <div>
          <p className="eyebrow">SmartHub Scan / {resolvedHubId}</p>
          <h1>Proof-of-Movement Scan</h1>
          <p>Capture GPS proof for {parcelId} and send it to the backend ImmuneNet validator.</p>
        </div>
        <span className="mono-chip">{status}</span>
      </section>

      <section className="command-grid">
        <section className="module-card">
          <div className="module-card__header">
            <div>
              <p>Phone GPS</p>
              <h2>Scan Payload</h2>
            </div>
            <span className="mono-chip">{parcelId}</span>
          </div>
          <div className="detail-stack">
            <p><strong>Hub:</strong> {resolvedHubId}</p>
            <p><strong>Lat:</strong> {gps.lat.toFixed(4)}</p>
            <p><strong>Lng:</strong> {gps.lng.toFixed(4)}</p>
            <p><strong>Accuracy:</strong> {Math.round(gps.accuracy_m)}m</p>
          </div>
          <div className="demo-control-groups">
            <button className="demo-action" onClick={captureBrowserGps} type="button">Capture GPS</button>
            <button className="demo-action" onClick={() => setGps(validGps)} type="button">Use Valid Fallback</button>
            <button className="demo-action demo-action--injectFakeScan" onClick={() => setGps(fakeGps)} type="button">Use Fake Fallback</button>
            <button className="demo-action demo-action--acceptScan" disabled={isLoading} onClick={submitScan} type="button">
              {isLoading ? 'Submitting...' : 'Submit Scan'}
            </button>
          </div>
        </section>

        <section className="module-card">
          <div className="module-card__header">
            <div>
              <p>ImmuneNet Decision</p>
              <h2>Scan Result</h2>
            </div>
            <span className={`mono-chip ${result?.led === 'GREEN' ? '' : 'mono-chip--warning'}`}>
              {result?.led || 'PENDING'}
            </span>
          </div>
          {result ? (
            <div className="detail-stack">
              <p><strong>Decision:</strong> {result.decision}</p>
              <p><strong>Action:</strong> {result.action}</p>
              <p><strong>LED:</strong> {result.led}</p>
              <p><strong>Reason:</strong> {result.reason}</p>
              <p><strong>Failed checks:</strong> {(result.failed_checks || []).join(', ') || 'None'}</p>
            </div>
          ) : (
            <p className="module-card__copy">No scan submitted yet.</p>
          )}
        </section>
      </section>
    </main>
  );
}
