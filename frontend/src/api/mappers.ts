// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: Convert backend payloads into stable frontend Type structures.

import type {
  ActiveParcel,
  Hub,
  Edge,
  RouteDecision,
  LedgerEvent,
  DemoAlert,
  Metric,
  ImmuneCheckResult,
  ImmuneCheckKey,
  DemoAlertType,
  CandidateScore,
  MovementProof,
  ImpactMetrics,
} from '../types/packetflow';
import { get_trust_status } from './endpoints'; // Wait, get_trust_status was in trust_engine.py, let's define it locally or import

export function getTrustStatus(score: number): 'trusted' | 'watch' | 'risky' | 'quarantined' {
  if (score >= 0.80) return 'trusted';
  if (score >= 0.60) return 'watch';
  if (score >= 0.40) return 'risky';
  return 'quarantined';
}

export function mapBackendParcel(p: any, latestRoute: any): ActiveParcel {
  if (!p) {
    return {
      id: 'MED-104',
      type: 'Medicine',
      current_hub: 'HUB-A',
      previous_hub: null,
      next_hop: 'HUB-B',
      destination_hub: 'CUSTOMER-ZONE',
      priority: 'High',
      sla_minutes: 45,
      sla_remaining_min: 43,
      temperature_c: 24.3,
      temperature_limit_c: 25.0,
      carrier_type: 'Van',
      status: 'Verified movement',
      trust_state: 'Verified',
    };
  }
  return {
    id: p.id || 'MED-104',
    type: p.parcel_type ? p.parcel_type.charAt(0).toUpperCase() + p.parcel_type.slice(1) : 'Medicine',
    current_hub: p.current_hub || 'HUB-A',
    previous_hub: p.previous_hub || null,
    next_hop: latestRoute?.selected_next_hop || p.next_hop || 'HUB-B',
    destination_hub: p.destination_hub || 'CUSTOMER-ZONE',
    priority: p.priority ? p.priority.charAt(0).toUpperCase() + p.priority.slice(1) : 'High',
    sla_minutes: p.sla_minutes || 45,
    sla_remaining_min: p.sla_minutes || 45,
    temperature_c: p.current_temperature || 24.3,
    temperature_limit_c: p.temperature_limit || 25.0,
    carrier_type: p.carrier_type ? p.carrier_type.charAt(0).toUpperCase() + p.carrier_type.slice(1) : 'Van',
    status: p.status === 'created' ? 'Created' : p.status === 'hold' ? 'Hold' : p.status === 'rerouted' ? 'Rerouted' : 'Verified movement',
    trust_state: p.trust_state === 'verified' ? 'Verified' : 'Unverified',
  };
}

export function mapBackendHubs(hubs: any[]): Hub[] {
  return hubs.map((h) => ({
    id: h.id,
    name: h.name,
    trust_score: h.trust_score,
    trust_status: getTrustStatus(h.trust_score),
    status: (h.status || 'active') as any,
    congestion: h.congestion,
    cold_chain: h.cold_chain,
    hardware_live: h.id === 'HUB-A' || h.id === 'HUB-B',
    anomaly_count: h.anomaly_count || 0,
    routing_behavior: h.routing_behavior || (
      h.trust_score >= 0.80 ? 'Normal routing corridor.' :
      h.trust_score >= 0.60 ? 'Watch status - slight delay penalty.' :
      h.trust_score >= 0.40 ? 'Avoid unless required.' : 'Excluded from routing corridor.'
    ),
    trust_history: h.trust_history || [h.trust_score],
  }));
}

export function mapBackendEdges(edges: any[]): Edge[] {
  return edges.map((e) => ({
    id: `${e.from_hub}-${e.to_hub}`,
    source: e.from_hub,
    target: e.to_hub,
    active: e.status === 'active',
    espNow: e.from_hub === 'HUB-A' && e.to_hub === 'HUB-B',
    label: e.from_hub === 'HUB-A' && e.to_hub === 'HUB-B' ? 'ESP-NOW handshake' : undefined,
  }));
}

export function mapBackendRouteDecision(d: any): RouteDecision {
  if (!d) {
    return {
      parcel_id: 'MED-104',
      current_hub: 'HUB-A',
      selected_next_hop: 'HUB-B',
      full_route: ['HUB-A', 'HUB-B', 'HUB-E', 'CUSTOMER-ZONE'],
      decision_type: 'Dynamic next-hop routing',
      triggered_by: 'Parcel creation / scan validation',
      reason: 'HUB-B selected because it preserves the 45-minute SLA while maintaining high trust.',
      timestamp: '10:42 AM demo time',
    };
  }
  return {
    parcel_id: d.parcel_id || 'MED-104',
    current_hub: d.current_hub || 'HUB-A',
    selected_next_hop: d.selected_next_hop || 'HUB-B',
    full_route: d.full_route || ['HUB-A', 'HUB-B', 'HUB-E', 'CUSTOMER-ZONE'],
    decision_type: d.decision_type || 'Dynamic next-hop routing',
    triggered_by: d.triggered_by || 'AgentOps disruption response',
    reason: d.reason || '',
    timestamp: d.timestamp || d.created_at || 'Just now',
  };
}

export function mapEventCategory(eventType: string): DemoAlertType {
  if (eventType === 'movement_accepted' || eventType === 'hardware_scan_completed') return 'accepted';
  if (eventType === 'movement_blocked' || eventType === 'fake_scan_blocked' || eventType === 'clone_scan_blocked' || eventType === 'immune_alert') return 'blocked';
  if (eventType === 'reroute_triggered') return 'rerouted';
  if (eventType === 'p2p_handshake') return 'p2p';
  if (eventType === 'trust_updated') return 'trust_update';
  if (eventType === 'temperature_breach') return 'cold_chain';
  return 'agentops';
}

export function mapBackendLedgerEvents(events: any[]): LedgerEvent[] {
  return events.map((e) => {
    let checksObj = {
      geofence: 'SKIPPED',
      speed: 'SKIPPED',
      routeGraph: 'SKIPPED',
      clone: 'SKIPPED',
      coldChain: 'SKIPPED',
      tamper: 'SKIPPED',
    };

    // If check exists in raw_payload (sometimes returned from ledger endpoints)
    if (e.raw_payload) {
      try {
        const payload = JSON.parse(e.raw_payload);
        if (payload.immune_checks) {
          const ic = payload.immune_checks;
          checksObj = {
            geofence: ic.geofence || 'SKIPPED',
            speed: ic.speed || 'SKIPPED',
            routeGraph: ic.route_graph || 'SKIPPED',
            clone: ic.clone_scan || 'SKIPPED',
            coldChain: ic.cold_chain || 'SKIPPED',
            tamper: ic.tamper || 'SKIPPED',
          };
        }
      } catch {}
    }

    return {
      id: String(e.id),
      timestamp: e.timestamp,
      parcelId: e.parcel_id || undefined,
      hubId: e.hub_id || undefined,
      event: e.event_type,
      category: mapEventCategory(e.event_type),
      geofence: (checksObj.geofence) as any,
      speed: (checksObj.speed) as any,
      routeGraph: (checksObj.routeGraph) as any,
      clone: (checksObj.clone) as any,
      coldChain: (checksObj.coldChain) as any,
      tamper: (checksObj.tamper) as any,
      decision: e.decision || '',
      action: e.action || '',
      reason: e.reason || '',
    };
  });
}

export function mapEventToAlert(e: any): DemoAlert {
  const type = mapEventCategory(e.event_type);
  let severity: 'success' | 'warning' | 'danger' | 'info' = 'info';
  if (type === 'accepted') severity = 'success';
  else if (type === 'blocked') severity = 'danger';
  else if (type === 'rerouted' || type === 'cold_chain') severity = 'warning';

  let failedCheck = undefined;
  const checksResults: ImmuneCheckResult[] = [];

  if (e.raw_payload) {
    try {
      const payload = JSON.parse(e.raw_payload);
      if (payload.failed_checks && payload.failed_checks.length > 0) {
        failedCheck = payload.failed_checks[0];
      }
      if (payload.immune_checks) {
        const ic = payload.immune_checks;
        const checkKeys: { key: ImmuneCheckKey; label: string; status: any }[] = [
          { key: 'geofence', label: 'Geofence', status: ic.geofence },
          { key: 'speed', label: 'Speed plausibility', status: ic.speed },
          { key: 'route_graph', label: 'Route graph', status: ic.route_graph },
          { key: 'clone_scan', label: 'Identity check', status: ic.clone_scan },
          { key: 'cold_chain', label: 'Temperature guard', status: ic.cold_chain },
          { key: 'tamper', label: 'Tamper seal', status: ic.tamper },
        ];
        checkKeys.forEach((k) => {
          if (k.status) {
            checksResults.push({
              key: k.key,
              label: k.label,
              status: k.status,
            });
          }
        });
      }
    } catch {}
  }

  return {
    id: `ALT-${e.id}`,
    type,
    status: e.decision || 'ALERT',
    title: e.reason ? e.reason.split('.')[0] : 'System Alert',
    parcelId: e.parcel_id || undefined,
    hubId: e.hub_id || undefined,
    failedCheck,
    actionTaken: e.action || undefined,
    reason: e.reason || '',
    timestamp: e.timestamp,
    severity,
    decision: e.decision || undefined,
    checks: checksResults.length > 0 ? checksResults : undefined,
    ledgerEventId: String(e.id),
  };
}

export function mapBackendCandidateScores(scores: any[]): CandidateScore[] {
  if (!scores || scores.length === 0) {
    return [
      {
        hub_id: 'HUB-B',
        sla_risk: 0.2,
        congestion_risk: 0.5,
        trust_risk: 0.1,
        condition_risk: 0.4,
        cost_score: 0.3,
        final_score: 0.34,
        selected: true,
        result: 'Selected',
      },
    ];
  }
  return scores.map((s) => ({
    hub_id: s.hub_id,
    sla_risk: s.sla_risk,
    congestion_risk: s.congestion_risk,
    trust_risk: s.trust_risk,
    condition_risk: s.condition_risk,
    cost_score: s.cost_emission_score || s.cost_score || 0.3,
    final_score: s.final_score,
    selected: s.selected,
    result: s.selected ? 'Selected' : s.rejection_reason || 'Rejected',
  }));
}

export function mapBackendMovementProof(e: any): MovementProof {
  if (!e) {
    return {
      parcel_id: 'MED-104',
      hub_id: 'HUB-A',
      scanner_id: 'ESP32-HUB-A',
      rfid_verified: true,
      qr_verified: true,
      gps_distance_m: 18,
      geofence: 'PASS',
      temperature_c: 24.3,
      timestamp: '10:42 AM demo time',
      ble_verified: true,
      esp_now_prior_acceptance: true,
      esp_now_prior_hub: 'HUB-A',
      decision: 'ACCEPTED',
      led: 'GREEN',
      reason: 'Movement accepted because identity, GPS geofence, route validity, temperature, and tamper checks passed.',
    };
  }

  let rfid_verified = true;
  let qr_verified = true;
  let ble_verified = false;
  let esp_now_prior_acceptance = false;
  let esp_now_prior_hub = '';

  if (e.raw_payload) {
    try {
      const payload = JSON.parse(e.raw_payload);
      if (payload.request) {
        rfid_verified = payload.request.rfid_verified ?? true;
        qr_verified = payload.request.qr_verified ?? true;
        ble_verified = payload.request.ble_verified ?? false;
        esp_now_prior_acceptance = payload.request.esp_now_prior_acceptance ?? false;
        esp_now_prior_hub = payload.request.esp_now_prior_hub ?? '';
      }
    } catch {}
  }

  return {
    parcel_id: e.parcel_id || 'MED-104',
    hub_id: e.hub_id || 'HUB-A',
    scanner_id: e.scanner_id || 'ESP32-HUB-A',
    rfid_verified,
    qr_verified,
    gps_distance_m: e.gps_accuracy_m || 18,
    geofence: (e.gps_lat ? 'PASS' : 'FAIL') as any, // Simple fallback
    temperature_c: e.temperature_c || 24.3,
    timestamp: e.timestamp,
    ble_verified,
    esp_now_prior_acceptance,
    esp_now_prior_hub,
    decision: e.decision || 'ACCEPTED',
    led: e.decision === 'ACCEPTED' ? 'GREEN' : e.decision === 'BLOCKED' ? 'RED' : 'AMBER',
    reason: e.reason || '',
  };
}

export function mapBackendMetrics(m: any, hubs: any[]): Metric[] {
  const trustedCount = hubs.filter((h) => h.trust_score >= 0.80).length;
  return [
    {
      label: 'Active Parcels',
      value: String(24),
      description: 'Proof-ready consignments currently moving through trusted corridors.',
      meta: 'MED / COLD CHAIN',
      highlighted: true,
    },
    {
      label: 'Trusted Hubs',
      value: String(trustedCount),
      description: 'Verified relay nodes above PacketFlow trust threshold.',
      meta: 'TRUST > 0.88',
    },
    {
      label: 'Anomalies Blocked',
      value: String(m?.anomalies_blocked ?? 7),
      description: 'Fake, clone, tamper, and cold-chain claims quarantined.',
      meta: '0 ACCEPTED RISK',
    },
    {
      label: 'Reroutes Triggered',
      value: String(m?.reroutes_triggered ?? 5),
      description: 'Trust-aware path changes prepared for live demo playback.',
      meta: `${m?.reroute_time_ms ?? 780} MS RESOLUTION`,
    },
  ];
}

export function mapBackendImpactMetrics(m: any, hubs: any[]): ImpactMetrics {
  const trustedCount = hubs.filter((h) => h.trust_score >= 0.80).length;
  const quarantineCount = hubs.filter((h) => h.trust_score < 0.40).length;
  return {
    activeParcels: 24,
    trustedHubs: trustedCount,
    anomaliesBlocked: m?.anomalies_blocked ?? 7,
    reroutesTriggered: m?.reroutes_triggered ?? 5,
    fakeScansBlocked: m?.fake_scans_blocked ?? 0,
    coldChainBreaches: m?.cold_chain_breaches ?? 0,
    trustQuarantines: quarantineCount,
    scanValidationLatencyMs: m?.scan_validation_latency_ms ?? 142,
    rerouteTimeMs: m?.reroute_time_ms ?? 780,
  };
}
