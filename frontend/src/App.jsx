// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: Top-level command center placeholder.

import AppShell from './components/layout/AppShell.jsx';

export default function App() {
  return (
    <AppShell>
      <main className="dashboard-grid">
        <section className="hero-panel">
          <p className="eyebrow">Team Aristotle</p>
          <h1>VeriRoute Nexus</h1>
          <p>Proof-powered routing for trusted logistics</p>
        </section>
        <section className="panel"><h2>Dashboard</h2><p>TODO: Show parcel state and demo controls.</p></section>
        <section className="panel"><h2>Digital Twin</h2><p>TODO: Show hubs, parcels, and live route updates.</p></section>
        <section className="panel"><h2>Alerts</h2><p>TODO: Show ImmuneNet and cold-chain events.</p></section>
        <section className="panel"><h2>Trust Board</h2><p>TODO: Show hub-level trust.</p></section>
      </main>
    </AppShell>
  );
}
