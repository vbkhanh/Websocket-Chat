from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine, create_async_engine, AsyncSession
)
from sqlalchemy.orm import (
    sessionmaker, declarative_base
)

from app.settings import settings


BaseModel = declarative_base()


async_engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_MAX,
    future=True
)

sess = sessionmaker(     
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    future=True,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sess() as session:
        yield session
