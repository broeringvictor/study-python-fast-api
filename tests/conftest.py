import pytest
import pytest_asyncio
from typing import AsyncGenerator

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import table_registry
from app.db.db_context import get_session
from tests.factory.user import UserFactory


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    async with engine.begin() as conn:  # type: ignore[arg-type]  
        await conn.run_sync(table_registry.metadata.create_all)

    yield

    async with engine.begin() as conn:  # type: ignore[arg-type]  
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session(setup_db) -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def client(setup_db):
    async def get_session_override():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_on_db(session):
    user = UserFactory.build()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def token(client, user_on_db):
    response = client.post(
        "/auth/",
        json={
            "email": user_on_db.email,
            "password": "DefaultP@ssw0rd!",
        },
    )
    assert response.status_code == 200
    return response.cookies.get("access_token")