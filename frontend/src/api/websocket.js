// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: WebSocket connection helper.

export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export function connectDemoSocket(onMessage) {
  const socket = new WebSocket(WS_URL);
  socket.onmessage = (event) => onMessage(JSON.parse(event.data));
  return socket;
}
