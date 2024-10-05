import asyncio
from typing import Iterator

import dotenv
import pytest_asyncio
from _pytest.fixtures import FixtureRequest
from sqlalchemy import NullPool

from hew_back.util import keycloak

dotenv.load_dotenv("./.env.test")
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from hew_back import main, ENV, responses, deps
from hew_back.db import BaseTable, DB
from test.base import Client


@pytest.fixture(scope="session")
def event_loop(request: FixtureRequest) -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.__original_fixture_loop = True  # type: ignore[attr-defined]
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app():
    return main.app


@pytest.fixture(scope="session")
def engine(event_loop):
    engine = create_async_engine(ENV.database.db_url, echo=False, poolclass=NullPool)
    try:
        yield engine
    finally:
        engine.sync_engine.dispose()


@pytest_asyncio.fixture
async def create(engine):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.create_all)
        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(BaseTable.metadata.drop_all)


@pytest_asyncio.fixture
async def session(engine, create, app):
    session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async def override_get_db():
        async with session_maker() as db_session:
            yield db_session

    app.dependency_overrides[deps.DbDeps.session] = override_get_db

    async with session_maker() as session:
        yield session


@pytest.fixture
def client(app):
    return Client(app)


@pytest.fixture
def keycloak_user_profile() -> keycloak.KeycloakUserProfile:
    return keycloak.KeycloakUserProfile(
        sub="7f4b560a-71f1-4c19-a003-3c42eb0899e3",
        email_verified=True,
        preferred_username="username",
        email="test@example.com",
    )


@pytest.fixture
def token_info(keycloak_user_profile, session) -> responses.TokenInfo:
    return responses.TokenInfo.create_access_token(
        keycloak_user_profile
    )
