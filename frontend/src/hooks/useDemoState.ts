import { useMemo, useState } from 'react';
import {
  activeParcel,
  candidateScores,
  metrics,
  movementProof,
  routeDecision,
  twinEdges,
  twinHubs,
} from '../data/mockData';
import type {
  ActiveParcel,
  AgentOpsEvent,
  ColdChainState,
  DemoAlert,
  Edge,
  Hub,
  ImpactMetrics,
  LedgerEvent,
  Metric,
  MovementProof,
  RouteDecision,
} from '../types/packetflow';
import { createDemoAlert, getDemoTimestamp } from '../utils/demoActions.ts';
import {
  acceptedScanChecks,
  attachAuditDetails,
  coldChainChecks,
  createLedgerEvent,
  fakeScanChecks,
  p2pChecks,
  rerouteChecks,
} from '../utils/eventMappers.ts';

const initialActiveRoute = ['HUB-A', 'HUB-B', 'HUB-E', 'CUSTOMER-ZONE'];
const alternateColdRoute = ['HUB-A', 'HUB-C', 'COLD-HUB-C', 'HUB-E', 'CUSTOMER-ZONE'];
const baselineImpactMetrics: ImpactMetrics = {
  activeParcels: 24,
  trustedHubs: 18,
  anomaliesBlocked: 7,
  reroutesTriggered: 5,
  fakeScansBlocked: 0,
  coldChainBreaches: 0,
  trustQuarantines: 0,
  scanValidationLatencyMs: 142,
  rerouteTimeMs: 780,
};

let ledgerSequence = 0;

function cloneMetrics(): Metric[] {
  return metrics.map((metric) => ({ ...metric }));
}

function updateMetricValue(items: Metric[], label: string, updater: (value: number) => number) {
  return items.map((metric) => {
    if (metric.label !== label) return metric;
    const current = Number(metric.value);
    return { ...metric, value: String(updater(Number.isFinite(current) ? current : 0)) };
  });
}

function createEventId() {
  ledgerSequence += 1;
  return `EVT-${String(ledgerSequence).padStart(3, '0')}`;
}

export function useDemoState() {
  const [hubs, setHubs] = useState<Hub[]>(() => twinHubs.map((hub) => ({ ...hub })));
  const [edges] = useState<Edge[]>(() => twinEdges.map((edge) => ({ ...edge })));
  const [activeRoute, setActiveRoute] = useState<string[]>(initialActiveRoute);
  const [parcel, setParcel] = useState<ActiveParcel>({ ...activeParcel });
  const [currentRouteDecision, setRouteDecision] = useState<RouteDecision>({ ...routeDecision });
  const [currentMovementProof, setMovementProof] = useState<MovementProof>({ ...movementProof });
  const [alerts, setAlerts] = useState<DemoAlert[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<DemoAlert | null>(null);
  const [ledgerEvents, setLedgerEvents] = useState<LedgerEvent[]>([]);
  const [agentOpsEvent, setAgentOpsEvent] = useState<AgentOpsEvent>(null);
  const [coldChainState, setColdChainState] = useState<ColdChainState>(null);
  const [pulseHandshake, setPulseHandshake] = useState(false);
  const [currentMetrics, setMetrics] = useState<Metric[]>(cloneMetrics);
  const [impactMetrics, setImpactMetrics] = useState<ImpactMetrics>(baselineImpactMetrics);
  const [toast, setToast] = useState<string | null>(null);

  const selectedCandidateScores = useMemo(() => candidateScores.map((candidate) => ({ ...candidate })), []);

  function pushAlert(alert: DemoAlert) {
    setAlerts((items) => [alert, ...items].slice(0, 6));
    setSelectedAlert(alert);
  }

  function pushLedgerEvent(event: LedgerEvent) {
    setLedgerEvents((items) => [event, ...items].slice(0, 12));
  }

  function showToast(message: string) {
    setToast(message);
  }

  function replayHandshakePulse() {
    setPulseHandshake(false);
    window.setTimeout(() => setPulseHandshake(true), 20);
    window.setTimeout(() => setPulseHandshake(false), 1700);
  }

  function acceptScan() {
    const event = createLedgerEvent({
      id: createEventId(),
      parcelId: parcel.id,
      hubId: 'HUB-A',
      event: 'accepted_movement',
      category: 'accepted',
      decision: 'ACCEPTED',
      action: 'LED_GREEN_AND_ROUTE_AUTHORISED',
      reason: 'RFID, QR, GPS geofence, temperature, BLE, and ESP-NOW checks passed.',
      checks: {
        geofence: 'PASS',
        speed: 'PASS',
        routeGraph: 'PASS',
        clone: 'PASS',
        coldChain: 'PASS',
        tamper: 'PASS',
      },
    });
    setMovementProof((proof) => ({ ...proof, decision: 'ACCEPTED', led: 'GREEN' }));
    setParcel((item) => ({ ...item, status: 'Verified movement', trust_state: 'Verified' }));
    pushLedgerEvent(event);
    pushAlert(
      attachAuditDetails(
        createDemoAlert({
        type: 'accepted',
        status: 'ACCEPTED',
        title: 'Movement verified at HUB-A',
        parcelId: parcel.id,
        hubId: 'HUB-A',
        reason: 'Identity, GPS geofence, route validity, temperature, and tamper checks passed.',
        severity: 'success',
        decision: 'ACCEPTED',
        actionTaken: 'LED_GREEN_AND_ROUTE_AUTHORISED',
        checks: acceptedScanChecks,
      }),
        event,
      ),
    );
    showToast('SmartHub scan accepted.');
  }

  function triggerHandshake() {
    const event = createLedgerEvent({
      id: createEventId(),
      parcelId: parcel.id,
      hubId: 'HUB-B',
      event: 'p2p_handshake',
      category: 'p2p',
      decision: 'PRE-AUTHORISED',
      action: 'CACHE_TRUST_HANDOFF',
      reason: 'HUB-A pre-authorised MED-104 before HUB-B received the parcel.',
      checks: { routeGraph: 'PASS' },
    });
    replayHandshakePulse();
    setMovementProof((proof) => ({
      ...proof,
      esp_now_prior_acceptance: true,
      esp_now_prior_hub: 'HUB-A',
    }));
    pushLedgerEvent(event);
    pushAlert(
      attachAuditDetails(
        createDemoAlert({
        type: 'p2p',
        status: 'P2P HANDSHAKE',
        title: 'HUB-A pre-authorised MED-104 for HUB-B',
        parcelId: parcel.id,
        hubId: 'HUB-B',
        reason: 'Inter-hub trust moved before the parcel arrived.',
        severity: 'info',
        decision: 'PRE-AUTHORISED',
        actionTaken: 'CACHE_TRUST_HANDOFF',
        checks: p2pChecks,
      }),
        event,
      ),
    );
    showToast('ESP-NOW handshake received.');
  }

  function injectFakeScan() {
    const event = createLedgerEvent({
      id: createEventId(),
      parcelId: parcel.id,
      hubId: 'HUB-C',
      event: 'fake_scan_blocked',
      category: 'blocked',
      decision: 'BLOCKED',
      action: 'QUARANTINE_MOVEMENT_CLAIM',
      reason: 'Scanner GPS was outside HUB-C geofence.',
      checks: {
        geofence: 'FAIL',
        speed: 'PASS',
        routeGraph: 'PASS',
        clone: 'PASS',
        coldChain: 'PASS',
        tamper: 'PASS',
      },
    });
    setHubs((items) =>
      items.map((hub) =>
        hub.id === 'HUB-C'
          ? {
              ...hub,
              trust_score: 0.35,
              trust_status: 'quarantined',
              anomaly_count: hub.anomaly_count + 1,
              routing_behavior: 'Excluded from routing until trust recovers.',
              trust_history: [...(hub.trust_history ?? [0.5]), 0.35],
            }
          : hub,
      ),
    );
    setMovementProof((proof) => ({
      ...proof,
      decision: 'BLOCKED',
      led: 'RED',
      geofence: 'FAIL',
      reason: 'Scanner GPS was outside HUB-C geofence.',
    }));
    setMetrics((items) =>
      updateMetricValue(
        updateMetricValue(items, 'Anomalies Blocked', (value) => value + 1),
        'Trusted Hubs',
        (value) => Math.max(0, value - 1),
      ),
    );
    setImpactMetrics((items) => ({
      ...items,
      trustedHubs: Math.max(0, items.trustedHubs - (items.trustQuarantines === 0 ? 1 : 0)),
      anomaliesBlocked: items.anomaliesBlocked + 1,
      fakeScansBlocked: items.fakeScansBlocked + 1,
      trustQuarantines: Math.max(items.trustQuarantines, 1),
    }));
    pushLedgerEvent(event);
    pushAlert(
      attachAuditDetails(
        createDemoAlert({
        type: 'blocked',
        status: 'BLOCKED',
        title: 'Fake scan rejected at HUB-C',
        parcelId: parcel.id,
        hubId: 'HUB-C',
        failedCheck: 'Geofence',
        actionTaken: 'QUARANTINE_MOVEMENT_CLAIM',
        reason: 'Scanner GPS was outside HUB-C geofence.',
        severity: 'danger',
        decision: 'BLOCKED',
        trustDelta: -0.15,
        checks: fakeScanChecks,
      }),
        event,
      ),
    );
    pushAlert(
      createDemoAlert({
        type: 'trust_update',
        status: 'TRUST UPDATE',
        title: 'HUB-C trust decayed to 0.35',
        hubId: 'HUB-C',
        actionTaken: 'EXCLUDE_FROM_ROUTING',
        reason: 'Repeated anomaly evidence lowered HUB-C below quarantine threshold.',
        severity: 'danger',
        decision: 'QUARANTINED',
        trustDelta: -0.15,
      }),
    );
    showToast('Fake scan blocked by ImmuneNet.');
  }

  function applyReroute(reason: string, status: string, title: string, eventName: string) {
    const event = createLedgerEvent({
      id: createEventId(),
      parcelId: parcel.id,
      hubId: 'HUB-B',
      event: eventName,
      category: 'rerouted',
      decision: 'REROUTED',
      action: 'PACKETFLOW_REPLAN_ROUTE',
      reason,
      checks: {
        geofence: 'PASS',
        speed: 'PASS',
        routeGraph: 'PASS',
        clone: 'PASS',
        coldChain: 'PASS',
        tamper: 'PASS',
      },
    });
    setActiveRoute(alternateColdRoute);
    setRouteDecision((decision) => ({
      ...decision,
      selected_next_hop: 'HUB-C',
      full_route: alternateColdRoute,
      triggered_by: 'AgentOps disruption response',
      reason,
      timestamp: getDemoTimestamp(),
    }));
    setParcel((item) => ({ ...item, next_hop: 'HUB-C' }));
    setMetrics((items) => updateMetricValue(items, 'Reroutes Triggered', (value) => value + 1));
    setImpactMetrics((items) => ({ ...items, reroutesTriggered: items.reroutesTriggered + 1 }));
    setAgentOpsEvent({
      title,
      detail: reason,
      timestamp: getDemoTimestamp(),
    });
    pushLedgerEvent(event);
    pushAlert(
      attachAuditDetails(
        createDemoAlert({
        type: 'rerouted',
        status,
        title,
        parcelId: parcel.id,
        hubId: 'HUB-B',
        actionTaken: 'PACKETFLOW_REPLAN_ROUTE',
        reason,
        severity: 'warning',
        decision: 'REROUTED',
        routeChange: alternateColdRoute,
        checks: rerouteChecks,
      }),
        event,
      ),
    );
  }

  function failHubB() {
    setHubs((items) => items.map((hub) => (hub.id === 'HUB-B' ? { ...hub, status: 'failed' } : hub)));
    applyReroute(
      'HUB-B failed, so PacketFlow selected the cold-chain recovery path.',
      'REROUTED',
      'HUB-B failed, route self-healed',
      'hub_failed_reroute',
    );
    showToast('Route replanned after HUB-B failure.');
  }

  function overloadHubB() {
    setHubs((items) => items.map((hub) => (hub.id === 'HUB-B' ? { ...hub, status: 'overloaded' } : hub)));
    applyReroute(
      'HUB-B overloaded, so PacketFlow selected an alternate SLA-safe path.',
      'REROUTED',
      'HUB-B overloaded',
      'hub_overloaded_reroute',
    );
    showToast('AgentOps triggered reroute.');
  }

  function raiseTemperature() {
    const event = createLedgerEvent({
      id: createEventId(),
      parcelId: parcel.id,
      hubId: 'HUB-A',
      event: 'temperature_breach_reroute',
      category: 'cold_chain',
      decision: 'REROUTED',
      action: 'REROUTE_TO_COLD_HUB',
      reason: 'MED-104 exceeded 25°C, so PacketFlow rerouted it to COLD-HUB-C.',
      checks: {
        geofence: 'PASS',
        speed: 'PASS',
        routeGraph: 'PASS',
        clone: 'PASS',
        coldChain: 'FAIL',
        tamper: 'PASS',
      },
    });
    setParcel((item) => ({ ...item, temperature_c: 29.2, next_hop: 'COLD-HUB-C' }));
    setMovementProof((proof) => ({ ...proof, temperature_c: 29.2 }));
    setColdChainState({
      current_temperature_c: 29.2,
      limit_c: 25,
      status: 'Cold-chain risk detected',
      action: 'Reroute to COLD-HUB-C',
    });
    setActiveRoute(alternateColdRoute);
    setRouteDecision((decision) => ({
      ...decision,
      selected_next_hop: 'COLD-HUB-C',
      full_route: alternateColdRoute,
      reason: 'MED-104 exceeded 25°C, so PacketFlow rerouted it to COLD-HUB-C.',
      triggered_by: 'Cold-chain breach',
      timestamp: getDemoTimestamp(),
    }));
    setMetrics((items) => updateMetricValue(items, 'Reroutes Triggered', (value) => value + 1));
    setImpactMetrics((items) => ({
      ...items,
      coldChainBreaches: items.coldChainBreaches + 1,
      reroutesTriggered: items.reroutesTriggered + 1,
    }));
    pushLedgerEvent(event);
    pushAlert(
      attachAuditDetails(
        createDemoAlert({
        type: 'cold_chain',
        status: 'REROUTED',
        title: 'Cold-chain risk detected',
        parcelId: parcel.id,
        hubId: 'COLD-HUB-C',
        failedCheck: 'Temperature',
        actionTaken: 'REROUTE_TO_COLD_HUB',
        reason: 'MED-104 exceeded 25°C, so PacketFlow rerouted it to COLD-HUB-C.',
        severity: 'warning',
        decision: 'REROUTED',
        routeChange: alternateColdRoute,
        checks: coldChainChecks,
      }),
        event,
      ),
    );
    showToast('Cold-chain breach detected.');
  }

  function resetDemo() {
    setHubs(twinHubs.map((hub) => ({ ...hub })));
    setActiveRoute(initialActiveRoute);
    setParcel({ ...activeParcel });
    setRouteDecision({ ...routeDecision });
    setMovementProof({ ...movementProof });
    setAlerts([]);
    setSelectedAlert(null);
    setLedgerEvents([]);
    setAgentOpsEvent(null);
    setColdChainState(null);
    setPulseHandshake(false);
    setMetrics(cloneMetrics());
    setImpactMetrics(baselineImpactMetrics);
    showToast('Demo state reset.');
  }

  return {
    hubs,
    edges,
    activeRoute,
    parcel,
    routeDecision: currentRouteDecision,
    movementProof: currentMovementProof,
    candidateScores: selectedCandidateScores,
    alerts,
    selectedAlert,
    selectAlert: setSelectedAlert,
    ledgerEvents,
    agentOpsEvent,
    coldChainState,
    pulseHandshake,
    metrics: currentMetrics,
    impactMetrics,
    toast,
    acceptScan,
    triggerHandshake,
    injectFakeScan,
    failHubB,
    overloadHubB,
    raiseTemperature,
    resetDemo,
  };
}

export type DemoState = ReturnType<typeof useDemoState>;
