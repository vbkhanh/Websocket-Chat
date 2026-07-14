from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.websocket_manager import manager
from app.models import User, Message, Group
import json
from app.redis_pubsub import RedisPubSub
import asyncio
from starlette.websockets import WebSocketState


router = APIRouter(
    prefix="/ws"
)


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, group_name: str, db: AsyncSession = Depends(get_session)):
    redis_pubsub = RedisPubSub()

    await websocket.accept()

    # Validate group
    result = await db.scalars(select(Group.id).where(Group.name == group_name))
    group_id = result.first()
    
    if not group_id:
        await websocket.send_json({"error": "Invalid group name"})
        await websocket.close(code=1008)  # POLICY_VIOLATION
        return
    
    try:
        await redis_pubsub.connect()
        pubsub = await redis_pubsub.subscribe(group_name)
    except Exception as e:
        await websocket.send_json({"error": "Redis connection failed"})
        await websocket.close(code=1011)  # INTERNAL_ERROR
        return

    # One task for receiving messages from WebSocket and publishing to Redis
    async def sender():
        try:
            while True:
                data = await websocket.receive_json()
               

                username = data.get("username")
                message = data.get("message")
                
                if not username or not message:
                    await websocket.send_json({"error": "Username and message are required"})
                    continue

                result = await db.scalars(select(User.id).where(User.username == username))
                user_id = result.first()
                if not user_id:
                    await websocket.send_json({"error": f"User {username} not found"})
                    continue

                msg = Message(content=message, user_id=user_id, group_id=group_id)
                db.add(msg)
                await db.commit()

                await redis_pubsub.publish(group_name, {
                    "username": username,
                    "message": message
                })

        except WebSocketDisconnect:
            return

        except Exception as e:
           if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(
                    {"error": "Unexpected server error"}
                )
                await websocket.close(code=1011)

    # One task for listening to Redis and sending to WebSocket
    async def receiver():
        try:
            async for message in pubsub.listen():
                if message['type'] == 'message':
                    payload = json.loads(message['data'])
                    await websocket.send_json(payload)
        except Exception as e:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(
                    {"error": "Unexpected server error"}
                )
                await websocket.close(code=1011)

    try:
        sender_task = asyncio.create_task(sender())
        receiver_task = asyncio.create_task(receiver())

        done, pending = await asyncio.wait(
            {sender_task, receiver_task},
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

        await asyncio.gather(*pending, return_exceptions=True)

    finally:
        await redis_pubsub.unsubscribe(group_name)
        await redis_pubsub.close()
        

    # await manager.connect(group_name, websocket)
    # try:
    #     while True:
    #         raw_data = await websocket.receive_text()
    #         data = json.loads(raw_data)

    #         username = data.get("username")
    #         message = data.get("message")

    #         if not username or not message:
    #             continue

    #         # Get user
    #         result = await db.scalars(select(User.id).where(User.username == username))
    #         user_id = result.first()
            
    #         # Get group
    #         result = await db.scalars(select(Group.id).where(Group.name == group_name))
    #         group_id = result.first()
         
    #         if not user_id or not group_id:
    #             continue

    #         # Save to DB
    #         msg = Message(content=message, user_id=user_id, group_id=group_id)
    #         db.add(msg)
    #         await db.commit()

    #         # Broadcast to group
    #         await manager.broadcast(group_name, data)

    # except WebSocketDisconnect:
    #     manager.disconnect(group_name, websocket)