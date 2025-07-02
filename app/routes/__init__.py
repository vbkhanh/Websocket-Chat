from fastapi import APIRouter
from app.routes import (
    websocket_routes, group_routes, user_routes, message_routes
)


api_router = APIRouter()

api_router.include_router(websocket_routes.router, tags=["websocket"])
api_router.include_router(group_routes.router, tags=["groups"])
api_router.include_router(user_routes.router, tags=["users"])
api_router.include_router(message_routes.router, tags=["messages"])
