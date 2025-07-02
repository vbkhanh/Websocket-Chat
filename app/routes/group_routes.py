from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.schemas import GroupOut, GroupCreate
from app.models import Group

router = APIRouter(
    prefix="/groups"
)

@router.post("", response_model=GroupOut)
async def create_group(group_in: GroupCreate, db: AsyncSession = Depends(get_session)):
    result = await db.scalars(select(Group).where(Group.name == group_in.name))
    existing_group = result.first()
    if existing_group:
        raise HTTPException(status_code=400, detail="Group name already exists")

    group = Group(name=group_in.name)
    db.add(group)
    await db.commit()
    return group

@router.get("", response_model=list[GroupOut])
async def list_groups(db: AsyncSession = Depends(get_session)):
    result = await db.scalars(select(Group).order_by(Group.name))
    groups = result.all()
    return groups
