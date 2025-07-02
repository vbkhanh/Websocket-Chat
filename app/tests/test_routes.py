import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db import BaseModel, get_session
from app.models import Message, User, Group
from sqlalchemy.future import select

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/test_db"

@pytest_asyncio.fixture(scope="session")
def test_engine():
    return create_async_engine(TEST_DATABASE_URL, echo=True, future=True)

@pytest_asyncio.fixture(scope="session")
def test_sessionmaker(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(autouse=True)
async def override_get_session(test_engine, test_sessionmaker):
    async with test_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    async def _override_get_session():
        async with test_sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = _override_get_session
    yield
    await test_engine.dispose()

@pytest.mark.asyncio
async def test_create_user():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/users", json={"username": "testuser"})
            assert response.status_code == 201
            assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_create_group():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/groups", json={"name": "general"})
            assert response.status_code == 201
            assert response.json()["name"] == "general"


@pytest.mark.asyncio
async def test_list_groups():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/groups", json={"name": "general"})
            response = await ac.get("/groups")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert any(group["name"] == "general" for group in data)

@pytest.mark.asyncio
async def test_get_group_messages(test_sessionmaker):
    # Step 1: Create user & group
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            user_response = await ac.post("/users", json={"username": "khanh"})
            assert user_response.status_code == 201

            group_response = await ac.post("/groups", json={"name": "testgroup"})
            assert group_response.status_code == 201

    # Step 2: Insert message manually into DB
    async with test_sessionmaker() as session:
        user = await session.scalars(select(User).where(User.username == "khanh"))
        group = await session.scalars(select(Group).where(Group.name == "testgroup"))

        user = user.first()
        group = group.first()

        session.add(Message(content="Hello test history!", user_id=user.id, group_id=group.id))
        await session.commit()


    # Step 3: Fetch group messages
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get(f"/messages/{group.id}")
            assert response.status_code == 200
            messages = response.json()
            assert any(m["content"] == "Hello test history!" for m in messages)
