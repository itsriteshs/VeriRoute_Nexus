// Owner: Person 2 — Frontend + Digital Twin + UX Lead
// Purpose: React hook managing active WebSocket connections and status.

import { useCallback, useEffect, useRef, useState } from 'react';
import { PacketFlowSocket, type SocketStatus } from '../api/websocket';

export function usePacketFlowSocket(onMessage: (msg: any) => void) {
  const [status, setStatus] = useState<SocketStatus>('disconnected');
  const socketRef = useRef<PacketFlowSocket | null>(null);

  useEffect(() => {
    socketRef.current = new PacketFlowSocket(onMessage, (newStatus) => {
      setStatus(newStatus);
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, [onMessage]);

  const connect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.connect();
    }
  }, []);

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect();
    }
  }, []);

  return {
    status,
    connect,
    disconnect,
  };
}
