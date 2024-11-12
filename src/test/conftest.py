import asyncio
from typing import Iterator

import dotenv
import pytest_asyncio
from _pytest.fixtures import FixtureRequest
from sqlalchemy import NullPool

from hew_back.util import keycloak, tks

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from hew_back import main, ENV, deps, mdls
from hew_back.db import BaseTable
from test.base import Client

import uuid


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

from httpx import AsyncClient
@pytest_asyncio.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
def keycloak_user_profile() -> keycloak.KeycloakUserProfile:
    return keycloak.KeycloakUserProfile(
        sub="d89c7adb-74b2-f904-322e-70f642ee8132",
        email_verified=True,
        preferred_username="Ado",
        email="Ado@gmail.com",
    )


@pytest.fixture
def token_info(keycloak_user_profile, session) -> tks.TokenInfo:
    return mdls.JwtTokenData.new(
        token_type=mdls.TokenType.access,
        profile=keycloak_user_profile
    ).new_token_info(ENV.token.secret_key)


