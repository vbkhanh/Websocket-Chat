from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncEngine, create_async_engine, AsyncSession
)
from sqlalchemy.orm import (
    sessionmaker, declarative_base
)
from sqlalchemy import MetaData as _MetaData
from app.settings import settings

MetaData = _MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

BaseModel = declarative_base(metadata=MetaData)


async_engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_POOL_MAX,
    future=True
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    future=True,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
