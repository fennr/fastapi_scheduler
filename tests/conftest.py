import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.db import get_session
from app.main import app


@pytest.fixture(name='session')  #
async def session_fixture():  #

    engine = create_async_engine(
        'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres',
        # poolclass=StaticPool,
    )
    async with engine.connect() as conn:
        # await conn.begin()
        await conn.begin_nested()
        await conn.run_sync(SQLModel.metadata.create_all)
        AsyncSessionLocal = sessionmaker(
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )
        async with AsyncSessionLocal() as session:
            yield session
            await session.close()
            await conn.rollback()


@pytest.fixture(name='client')  #
async def client_fixture(session: Session):  #
    def get_session_override():  #
        return session

    app.dependency_overrides[get_session] = get_session_override  #
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()
