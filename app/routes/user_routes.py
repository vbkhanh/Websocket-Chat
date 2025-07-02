from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models import User
from app.schemas import UserCreate, UserOut

router = APIRouter(
     prefix="/users"
)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    # Check if username already exists
    result = await db.scalars(select(User).where(User.username == user_in.username))
    existing_user = result.first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create new user
    user = User(username=user_in.username)
    db.add(user)
    await db.commit()

    return user
