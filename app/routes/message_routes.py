from app.models import Message
from sqlalchemy import select
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import MessageOut

router = APIRouter(
    prefix="/messages"
)
@router.get("/{group_id}", response_model=list[MessageOut])
async def get_messages(group_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.scalars(select(Message).where(Message.group_id == group_id).order_by(Message.created_at.desc()).limit(50))
    messages = result.all()
    return messages