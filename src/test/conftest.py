import asyncio
import uuid

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from hew_back import main, model
from hew_back.db import BaseTable, DB
from test.base import Client


@pytest.fixture
def app():
    return main.app


@pytest.fixture
def client(app):
    return Client(app)


@pytest.fixture(scope="function")
def session_maker(app):
    db_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(db_url, echo=False)

    async def init_tables():
        async with engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.drop_all)
            await conn.run_sync(BaseTable.metadata.create_all)

    asyncio.run(init_tables())

    session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async def override_get_db():
        async with session_maker() as db_session:
            yield db_session

    app.dependency_overrides[DB.get_session] = override_get_db

    yield session_maker


@pytest.fixture
def keycloak_user_profile() -> model.KeycloakUserProfile:
    return model.KeycloakUserProfile(
        sub="7f4b560a-71f1-4c19-a003-3c42eb0899e3",
        email_verified=True,
        preferred_username="username",
        email="test@example.com",
    )


@pytest.fixture
def token_info(session_maker, keycloak_user_profile) -> model.TokenInfo:
    return model.TokenInfo.create_access_token(
        keycloak_user_profile
    )
