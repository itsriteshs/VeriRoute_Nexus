// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: Unified react hook for backend live state and WebSocket updates with mock fallback.

import { useCallback, useEffect, useState } from 'react';
import { useDemoState } from './useDemoState';
import { usePacketFlowSocket } from './usePacketFlowSocket';
import { apiGet, apiPost } from '../api/client';
import { endpoints } from '../api/endpoints';
import {
  mapBackendParcel,
  mapBackendHubs,
  mapBackendEdges,
  mapBackendRouteDecision,
  mapBackendLedgerEvents,
  mapEventToAlert,
  mapBackendCandidateScores,
  mapBackendMovementProof,
  mapBackendMetrics,
  mapBackendImpactMetrics,
} from '../api/mappers';
import { shouldUseWebSocket, type SocketStatus } from '../api/websocket';
import type { DemoState } from './useDemoState';

export type LiveDemoState = DemoState & {
  backendMode: 'live' | 'mock';
  websocketStatus: SocketStatus;
  lastEvent: string;
  syncBackend: () => Promise<void>;
  createMed104: () => Promise<void>;
  trafficJam: () => Promise<void>;
  weatherRisk: () => Promise<void>;
  cloneScan: () => Promise<void>;
  tamperEvent: () => Promise<void>;
  isOffline: boolean;
  unsyncedCount: number;
  toggleSync: () => Promise<void>;
  flushSync: () => Promise<void>;
  verifyChain: (parcelId: string) => Promise<any>;
};

export function usePacketFlowLiveState(): LiveDemoState {
  const mockState = useDemoState();

  const [backendMode, setBackendMode] = useState<'live' | 'mock'>('mock');
  const [lastEvent, setLastEvent] = useState<string>('Local initialization');
  const [wsStatus, setWsStatus] = useState<SocketStatus>('disconnected');
  const [isOffline, setIsOffline] = useState<boolean>(false);
  const [unsyncedCount, setUnsyncedCount] = useState<number>(0);

  // Live state variables
  const [hubs, setHubs] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [activeRoute, setActiveRoute] = useState<string[]>([]);
  const [parcel, setParcel] = useState<any>(null);
  const [routeDecision, setRouteDecision] = useState<any>(null);
  const [movementProof, setMovementProof] = useState<any>(null);
  const [candidateScores, setCandidateScores] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [selectedAlert, setSelectedAlert] = useState<any>(null);
  const [ledgerEvents, setLedgerEvents] = useState<any[]>([]);
  const [agentOpsEvent, setAgentOpsEvent] = useState<any>(null);
  const [coldChainState, setColdChainState] = useState<any>(null);
  const [pulseHandshake, setPulseHandshake] = useState(false);
  const [metrics, setMetrics] = useState<any[]>([]);
  const [impactMetrics, setImpactMetrics] = useState<any>(null);
  const [toast, setToast] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  const syncBackend = useCallback(async () => {
    try {
      const snapshot: any = await apiGet(endpoints.snapshot);
      if (snapshot) {
        const mappedRoute = mapBackendRouteDecision(snapshot.latest_route);
        setRouteDecision(mappedRoute);

        const mappedParcel = mapBackendParcel(snapshot.parcel, snapshot.latest_route);
        setParcel(mappedParcel);

        setActiveRoute(mappedRoute.full_route);

        const mappedHubs = mapBackendHubs(snapshot.hubs || []);
        setHubs(mappedHubs);
        setEdges(mapBackendEdges(snapshot.edges || []));

        setIsOffline(!!snapshot.is_offline);
        setUnsyncedCount(Number(snapshot.unsynced_count || 0));

        if (snapshot.latest_route?.candidate_scores) {
          try {
            const rawScores = typeof snapshot.latest_route.candidate_scores === 'string'
              ? JSON.parse(snapshot.latest_route.candidate_scores)
              : snapshot.latest_route.candidate_scores;
            setCandidateScores(mapBackendCandidateScores(rawScores));
          } catch {
            setCandidateScores(mapBackendCandidateScores([]));
          }
        } else {
          setCandidateScores(mapBackendCandidateScores([]));
        }

        const rawEvents = snapshot.recent_events || [];
        setLedgerEvents(mapBackendLedgerEvents(rawEvents));

        const scanEvent = rawEvents.find(
          (e: any) => e.event_type === 'scan_received' || e.event_type === 'hardware_scan_completed'
        );
        setMovementProof(mapBackendMovementProof(scanEvent));

        const alertEvents = rawEvents.filter(
          (e: any) =>
            e.event_type === 'fake_scan_blocked' ||
            e.event_type === 'clone_scan_blocked' ||
            e.event_type === 'temperature_breach' ||
            e.event_type === 'reroute_triggered'
        );
        const mappedAlerts = alertEvents.map((e: any) => mapEventToAlert(e));
        setAlerts(mappedAlerts);
        if (mappedAlerts.length > 0) {
          setSelectedAlert(mappedAlerts[0]);
        }

        setMetrics(mapBackendMetrics(snapshot.metrics, snapshot.hubs || []));
        setImpactMetrics(mapBackendImpactMetrics(snapshot.metrics, snapshot.hubs || []));

        const rerouteEvent = rawEvents.find((e: any) => e.event_type === 'reroute_triggered');
        if (rerouteEvent) {
          setAgentOpsEvent({
            title: rerouteEvent.reason ? rerouteEvent.reason.split('.')[0] : 'Reroute triggered',
            detail: rerouteEvent.reason || '',
            timestamp: rerouteEvent.timestamp,
          });
        } else {
          setAgentOpsEvent(null);
        }

        const breachEvent = rawEvents.find((e: any) => e.event_type === 'temperature_breach');
        if (breachEvent) {
          setColdChainState({
            current_temperature_c: mappedParcel.temperature_c,
            limit_c: mappedParcel.temperature_limit_c,
            status: 'Cold-chain risk detected',
            action: 'Reroute to COLD-HUB-C',
          });
        } else {
          setColdChainState(null);
        }
      }
    } catch (err) {
      console.error('Failed to sync backend:', err);
      showToast('Backend sync failed.');
    }
  }, []);

  useEffect(() => {
    async function checkHealth() {
      try {
        const res: any = await apiGet(endpoints.health);
        if (res && res.status === 'ok') {
          setBackendMode('live');
          await syncBackend();
        } else {
          setBackendMode('mock');
        }
      } catch {
        setBackendMode('mock');
      }
    }
    checkHealth();
  }, [syncBackend]);

  const handleSocketMessage = useCallback(
    (msg: any) => {
      if (!msg || !msg.type) return;
      setLastEvent(msg.type);

      if (msg.type === 'p2p_handshake') {
        setPulseHandshake(false);
        setTimeout(() => setPulseHandshake(true), 20);
        setTimeout(() => setPulseHandshake(false), 1700);
      }

      syncBackend();
    },
    [syncBackend]
  );

  const { status: currentWsStatus, connect, disconnect } = usePacketFlowSocket(handleSocketMessage);

  useEffect(() => {
    setWsStatus(currentWsStatus);
  }, [currentWsStatus]);

  useEffect(() => {
    if (backendMode === 'live' && shouldUseWebSocket()) {
      connect();
    } else {
      disconnect();
    }
    return () => disconnect();
  }, [backendMode, connect, disconnect]);

  useEffect(() => {
    let interval: number | null = null;
    if (backendMode === 'live' && (!shouldUseWebSocket() || wsStatus !== 'connected')) {
      interval = window.setInterval(() => {
        syncBackend();
      }, 2000);
    }
    return () => {
      if (interval) window.clearInterval(interval);
    };
  }, [backendMode, wsStatus, syncBackend]);

  const acceptScan = async () => {
    if (backendMode === 'mock') {
      mockState.acceptScan();
      setLastEvent('local_accept_scan');
      return;
    }
    try {
      await apiPost(endpoints.scan, {
        parcel_id: 'MED-104',
        hub_id: 'HUB-A',
        scanner_id: 'SCANNER-07',
        rfid_verified: true,
        qr_verified: true,
        gps: { lat: 11.0168, lng: 76.9558, accuracy_m: 18 },
        temperature_c: 24.3,
        carrier_type: 'van',
        tamper: false,
      });
      await syncBackend();
      showToast('Scan authorized on backend.');
    } catch (err) {
      console.error(err);
      showToast('Failed to accept scan on backend.');
    }
  };

  const triggerHandshake = async () => {
    if (backendMode === 'mock') {
      mockState.triggerHandshake();
      setLastEvent('local_p2p_handshake');
      return;
    }
    try {
      await apiPost(endpoints.p2pHandshake, {
        sender_hub: 'HUB-A',
        receiver_hub: 'HUB-B',
        parcel_id: 'MED-104',
        message_type: 'HUB_ACCEPTED',
        trust_delta: 0.01,
        eta_sec: 30,
        carrier_type: 'van',
      });
      await syncBackend();
      showToast('P2P handshake logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to log P2P handshake.');
    }
  };

  const injectFakeScan = async () => {
    if (backendMode === 'mock') {
      mockState.injectFakeScan();
      setLastEvent('local_fake_scan');
      return;
    }
    try {
      await apiPost(endpoints.fakeScan, {
        parcel_id: 'MED-104',
        claimed_hub: 'HUB-C',
        fake_gps: { lat: 11.1000, lng: 77.1000, accuracy_m: 20 },
      });
      await syncBackend();
      showToast('Fake scan rejected.');
    } catch (err) {
      console.error(err);
      showToast('Failed to inject fake scan.');
    }
  };

  const failHubB = async () => {
    if (backendMode === 'mock') {
      mockState.failHubB();
      setLastEvent('local_fail_hub');
      return;
    }
    try {
      await apiPost(endpoints.failHub, {
        hub_id: 'HUB-B',
        parcel_id: 'MED-104',
      });
      await syncBackend();
      showToast('HUB-B failed disruption logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to fail hub.');
    }
  };

  const overloadHubB = async () => {
    if (backendMode === 'mock') {
      mockState.overloadHubB();
      setLastEvent('local_overload_hub');
      return;
    }
    try {
      await apiPost(endpoints.overloadHub, {
        hub_id: 'HUB-B',
        parcel_id: 'MED-104',
        congestion: 0.95,
      });
      await syncBackend();
      showToast('HUB-B overload disruption logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to overload hub.');
    }
  };

  const raiseTemperature = async () => {
    if (backendMode === 'mock') {
      mockState.raiseTemperature();
      setLastEvent('local_temp_breach');
      return;
    }
    try {
      await apiPost(endpoints.tempBreach, {
        parcel_id: 'MED-104',
        hub_id: 'HUB-A',
        temperature_c: 29.2,
      });
      await syncBackend();
      showToast('Temperature breach logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to breach temp.');
    }
  };

  const createMed104 = async () => {
    if (backendMode === 'mock') {
      showToast('MED-104 is already loaded in local fallback mode.');
      setLastEvent('local_create_parcel');
      return;
    }
    try {
      await apiPost(endpoints.parcels, {
        id: 'MED-104',
        parcel_type: 'medicine',
        source_hub: 'HUB-A',
        destination_hub: 'CUSTOMER-ZONE',
        priority: 'high',
        sla_minutes: 45,
        temperature_limit: 25.0,
        carrier_type: 'van',
      });
      await syncBackend();
      showToast('MED-104 created and routed.');
    } catch (err) {
      console.error(err);
      showToast('Failed to create MED-104.');
    }
  };

  const trafficJam = async () => {
    if (backendMode === 'mock') {
      showToast('Traffic jam requires live backend mode.');
      setLastEvent('local_traffic_jam');
      return;
    }
    try {
      await apiPost(endpoints.trafficJam, {
        parcel_id: 'MED-104',
        from_hub: 'HUB-A',
        to_hub: 'HUB-B',
        traffic_risk: 0.85,
      });
      await syncBackend();
      showToast('Traffic disruption logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to trigger traffic jam.');
    }
  };

  const weatherRisk = async () => {
    if (backendMode === 'mock') {
      showToast('Weather risk requires live backend mode.');
      setLastEvent('local_weather_risk');
      return;
    }
    try {
      await apiPost(endpoints.weatherRisk, {
        parcel_id: 'MED-104',
        from_hub: 'HUB-A',
        to_hub: 'HUB-B',
        weather_risk: 0.9,
      });
      await syncBackend();
      showToast('Weather disruption logged.');
    } catch (err) {
      console.error(err);
      showToast('Failed to trigger weather risk.');
    }
  };

  const cloneScan = async () => {
    if (backendMode === 'mock') {
      showToast('Clone scan requires live backend mode.');
      setLastEvent('local_clone_scan');
      return;
    }
    try {
      await apiPost(endpoints.cloneScan, {
        parcel_id: 'MED-104',
        first_hub: 'HUB-B',
        second_hub: 'HUB-D',
      });
      await syncBackend();
      showToast('Clone scan blocked.');
    } catch (err) {
      console.error(err);
      showToast('Failed to trigger clone scan.');
    }
  };

  const tamperEvent = async () => {
    if (backendMode === 'mock') {
      showToast('Tamper event requires live backend mode.');
      setLastEvent('local_tamper_event');
      return;
    }
    try {
      await apiPost(endpoints.tamperScan, {
        parcel_id: 'MED-104',
        hub_id: 'HUB-C',
        tamper: true,
      });
      await syncBackend();
      showToast('Tamper event held.');
    } catch (err) {
      console.error(err);
      showToast('Failed to trigger tamper event.');
    }
  };

  const toggleSync = async () => {
    if (backendMode === 'mock') {
      showToast('Offline sync toggle requires live backend mode.');
      return;
    }
    try {
      const res: any = await apiPost('/demo/toggle-sync');
      if (res) {
        setIsOffline(res.is_offline);
        showToast(res.is_offline ? 'System simulated offline.' : 'System restored online.');
        await syncBackend();
      }
    } catch (err) {
      console.error(err);
      showToast('Failed to toggle sync.');
    }
  };

  const flushSync = async () => {
    if (backendMode === 'mock') {
      showToast('Offline flush requires live backend mode.');
      return;
    }
    try {
      const res: any = await apiPost('/demo/flush-sync');
      if (res) {
        setUnsyncedCount(0);
        showToast(`Flushed ${res.flushed_count} queued events to remote ledger.`);
        await syncBackend();
      }
    } catch (err) {
      console.error(err);
      showToast('Failed to flush sync.');
    }
  };

  const verifyChain = async (parcelId: string) => {
    if (backendMode === 'mock') {
      showToast('Ledger verification requires live backend mode.');
      return { verified: true, chain_length: 0, reason: 'Mock mode bypass' };
    }
    try {
      const res = await apiGet(`/ledger/verify/${parcelId}`);
      return res;
    } catch (err) {
      console.error(err);
      showToast('Failed to verify ledger chain.');
      return null;
    }
  };

  const resetDemo = async () => {
    if (backendMode === 'mock') {
      mockState.resetDemo();
      setLastEvent('local_reset');
      return;
    }
    try {
      await apiPost(endpoints.reset);
      await syncBackend();
      showToast('Backend state reset.');
    } catch (err) {
      console.error(err);
      showToast('Failed to reset backend.');
    }
  };

  if (backendMode === 'mock') {
    return {
      ...mockState,
      backendMode,
      websocketStatus: wsStatus,
      lastEvent,
      syncBackend,
      createMed104,
      trafficJam,
      weatherRisk,
      cloneScan,
      tamperEvent,
      isOffline: false,
      unsyncedCount: 0,
      toggleSync: async () => {},
      flushSync: async () => {},
      verifyChain: async () => ({ verified: true, chain_length: 0 }),
    } as LiveDemoState;
  }

  const liveHubs = hubs.length > 0 ? hubs : mockState.hubs;
  const liveEdges = edges.length > 0 ? edges : mockState.edges;
  const liveRouteDecision = routeDecision ?? mockState.routeDecision;
  const liveParcel = parcel ?? mockState.parcel;
  const liveActiveRoute = activeRoute.length > 0 ? activeRoute : liveRouteDecision.full_route;
  const liveMovementProof = movementProof ?? mockState.movementProof;
  const liveCandidateScores = candidateScores.length > 0 ? candidateScores : mockState.candidateScores;
  const liveMetrics = metrics.length > 0 ? metrics : mockState.metrics;
  const liveImpactMetrics = impactMetrics ?? mockState.impactMetrics;

  return {
    hubs: liveHubs,
    edges: liveEdges,
    activeRoute: liveActiveRoute,
    parcel: liveParcel,
    routeDecision: liveRouteDecision,
    movementProof: liveMovementProof,
    candidateScores: liveCandidateScores,
    alerts,
    selectedAlert: selectedAlert ?? mockState.selectedAlert,
    selectAlert: setSelectedAlert,
    ledgerEvents,
    agentOpsEvent,
    coldChainState,
    pulseHandshake,
    metrics: liveMetrics,
    impactMetrics: liveImpactMetrics,
    toast,
    acceptScan,
    triggerHandshake,
    injectFakeScan,
    failHubB,
    overloadHubB,
    raiseTemperature,
    resetDemo,
    backendMode,
    websocketStatus: wsStatus,
    lastEvent,
    syncBackend,
    createMed104,
    trafficJam,
    weatherRisk,
    cloneScan,
    tamperEvent,
    isOffline,
    unsyncedCount,
    toggleSync,
    flushSync,
    verifyChain,
  } as LiveDemoState;
}
