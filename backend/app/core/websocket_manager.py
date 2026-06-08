# Owner: Person 1 — Backend + Algorithms Lead
# Purpose: WebSocket connection manager for live event broadcasting.

import logging
from fastapi import WebSocket

logger = logging.getLogger("websocket_manager")


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    def get_connection_count(self) -> int:
        return len(self.active_connections)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")
                disconnected.append(connection)
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_event(self, event_type: str, payload: dict):
        from app.utils.time_utils import utc_now_iso
        envelope = {
            "type": event_type,
            "timestamp": utc_now_iso(),
            "payload": payload,
        }
        await self.broadcast(envelope)


websocket_manager = WebSocketManager()


async def safe_broadcast(event_type: str, payload: dict):
    try:
        await websocket_manager.broadcast_event(event_type, payload)
    except Exception as e:
        logger.error(f"Failed to safe broadcast {event_type}: {e}")
