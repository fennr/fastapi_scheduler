import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel
from sqlmodel.pool import StaticPool

from app.db import get_session
from app.main import app


@pytest.fixture(name='session')  #
async def session_fixture():  #

    engine = create_async_engine(
        'sqlite+aiosqlite:///test.sqlite3',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    AsyncSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(name='client')  #
async def client_fixture(session: Session):  #
    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override  #
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()
