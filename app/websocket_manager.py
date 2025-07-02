from typing import Dict, List
from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, group_name: str, websocket: WebSocket):
        await websocket.accept()
        if group_name not in self.active_connections:
            self.active_connections[group_name] = []
        self.active_connections[group_name].append(websocket)
        
    def disconnect(self, group_name: str, websocket: WebSocket):
        self.active_connections[group_name].remove(websocket)

    async def broadcast(self, group_name: str, message: dict):
        connections = self.active_connections.get(group_name, [])
        for connection in connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Broadcast error: {e}")

manager = ConnectionManager()
