import pytest
import sqlalchemy

from hew_back import model, table


@pytest.fixture
def post_user_body(session_maker) -> model.PostUserBody:
    return model.PostUserBody(
        user_name="PostUserBody_user_name"
    )


@pytest.mark.asyncio
async def test_create_gacha(session_maker, client, token_info,post_user_body):
    result = await client.post(
        "/api/user",
        post_user_body,
        token_info.token
    )
    assert result.status_code == 200, f"invalid status code {result.json()}"
    body = result.json()
    assert body is not None
    body = model.UserRes(**body)
    async with session_maker() as session:
        result = await session.execute(
            sqlalchemy.select(sqlalchemy.func.count())
            .select_from(table.UserTable)
            .where(table.UserTable.user_id == body.user_id)
        )
        assert result.scalar_one() == 1, f"\n{body}\n"
