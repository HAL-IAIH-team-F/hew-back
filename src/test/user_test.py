import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import result, tables, bodies, responses
from test.conftest import session


@pytest.fixture
def post_user_body(session) -> bodies.PostUserBody:
    return bodies.PostUserBody(
        user_name="PostUserBody_user_name",
        user_icon_uuid=None,
    )


@pytest_asyncio.fixture
async def post_user_body_saved(session, keycloak_user_profile) -> bodies.PostUserBody:
    body = bodies.PostUserBody(
        user_name="PostUserBody_user_name_saved",
        user_icon_uuid=None,
    )
    await body.save_new(session, keycloak_user_profile)
    return body


@pytest.mark.asyncio
async def test_create_user(session, client, token_info, post_user_body):
    result = await client.post(
        "/api/user",
        post_user_body,
        token_info.token
    )
    assert result.status_code == 200, f"invalid status code {result.json()}"
    body = result.json()
    assert body is not None
    body = responses.SelfUserRes(**body)
    result = await session.execute(
        sqlalchemy.select(sqlalchemy.func.count())
        .select_from(tables.UserTable)
        .where(tables.UserTable.user_id == body.user_id)
    )
    assert result.scalar_one() == 1, f"\n{body}\n"


@pytest.mark.asyncio
async def test_get_self(client, token_info, session, post_user_body_saved, keycloak_user_profile):
    result = await client.get(
        "/api/user/self",
        token_info.token
    )
    assert result.status_code == 200, f"invalid status code {result.read()}"
    body = result.json()
    assert body is not None
    body = responses.SelfUserRes(**body)
    assert body.user_id == keycloak_user_profile.sub
    assert body.user_mail == keycloak_user_profile.email
    assert body.user_name == post_user_body_saved.user_name
