// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: WebSocket manager with reconnection backoff and status callbacks.

function defaultWsUrl() {
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.host}/api/ws`;
  }
  return 'ws://localhost:8000/ws';
}

export const WS_URL = (import.meta.env.VITE_WS_URL as string) || defaultWsUrl();

export type SocketStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

export function shouldUseWebSocket() {
  if (import.meta.env.VITE_WS_URL) {
    return true;
  }
  if (typeof window === 'undefined') {
    return false;
  }
  return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
}

export class PacketFlowSocket {
  private socket: WebSocket | null = null;
  private status: SocketStatus = 'disconnected';
  private reconnectTimeout: number | null = null;
  private reconnectDelay = 1000;
  private maxReconnectDelay = 10000;

  constructor(
    private onMessage: (msg: any) => void,
    private onStatusChange: (status: SocketStatus) => void
  ) {}

  connect() {
    this.cleanup();
    this.setStatus('connecting');
    try {
      this.socket = new WebSocket(WS_URL);
      this.socket.onopen = () => {
        this.setStatus('connected');
        this.reconnectDelay = 1000; // reset delay
      };
      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (err) {
          console.error('WebSocket parse error:', err);
        }
      };
      this.socket.onerror = () => {
        this.setStatus('error');
      };
      this.socket.onclose = () => {
        if (this.status !== 'disconnected') {
          this.setStatus('disconnected');
          this.scheduleReconnect();
        }
      };
    } catch (err) {
      console.error('WebSocket connection error:', err);
      this.setStatus('error');
      this.scheduleReconnect();
    }
  }

  disconnect() {
    this.setStatus('disconnected');
    this.cleanup();
  }

  private setStatus(newStatus: SocketStatus) {
    this.status = newStatus;
    this.onStatusChange(newStatus);
  }

  private scheduleReconnect() {
    if (this.reconnectTimeout) return;
    this.reconnectTimeout = window.setTimeout(() => {
      this.reconnectTimeout = null;
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
      this.connect();
    }, this.reconnectDelay);
  }

  private cleanup() {
    if (this.reconnectTimeout) {
      window.clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }
}
export function connectDemoSocket(onMessage: (msg: any) => void) {
  const socket = new WebSocket(WS_URL);
  socket.onmessage = (event) => onMessage(JSON.parse(event.data));
  return socket;
}
