import pytest
import sqlalchemy

from hew_back import model, table


@pytest.fixture
def post_user_body(session_maker) -> model.PostUserBody:
    return model.PostUserBody(
        user_name="PostUserBody_user_name"
    )


@pytest.fixture
async def post_user_body_saved(session_maker, keycloak_user_profile) -> model.PostUserBody:
    tbl = model.PostUserBody(
        user_name="PostUserBody_user_name_saved"
    )
    async with session_maker() as session:
        tbl.new_record(session, keycloak_user_profile)
        await session.commit()
    return tbl


@pytest.mark.asyncio
async def test_create_user(session_maker, client, token_info, post_user_body):
    result = await client.post(
        "/api/user",
        post_user_body,
        token_info.token
    )
    assert result.status_code == 200, f"invalid status code {result.json()}"
    body = result.json()
    assert body is not None
    body = model.SelfUserRes(**body)
    async with session_maker() as session:
        result = await session.execute(
            sqlalchemy.select(sqlalchemy.func.count())
            .select_from(table.UserTable)
            .where(table.UserTable.user_id == body.user_id)
        )
        assert result.scalar_one() == 1, f"\n{body}\n"


@pytest.mark.asyncio
async def test_get_self(client, token_info, session_maker, post_user_body_saved, keycloak_user_profile):
    result = await client.get(
        "/api/user/self",
        token_info.token
    )
    assert result.status_code == 200, f"invalid status code {result.read()}"
    body = result.json()
    assert body is not None
    body = model.SelfUserRes(**body)
    assert body.user_id == keycloak_user_profile.sub
    assert body.user_mail == keycloak_user_profile.email
    assert body.user_name == post_user_body_saved.user_name
