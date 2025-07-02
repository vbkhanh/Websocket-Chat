from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.websocket_manager import manager
from app.models import User, Message, Group
import json

router = APIRouter(
    prefix="/ws"
)


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, group_name: str, db: AsyncSession = Depends(get_session)):
    await manager.connect(group_name, websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)

            username = data.get("username")
            message = data.get("message")

            if not username or not message:
                continue

            # Get user
            result = await db.scalars(select(User.id).where(User.username == username))
            user_id = result.first()
            
            # Get group
            result = await db.scalars(select(Group.id).where(Group.name == group_name))
            group_id = result.first()
         
            if not user_id or not group_id:
                continue

            # Save to DB
            msg = Message(content=message, user_id=user_id, group_id=group_id)
            db.add(msg)
            await db.commit()

            # Broadcast to group
            await manager.broadcast(group_name, data)

    except WebSocketDisconnect:
        manager.disconnect(group_name, websocket)