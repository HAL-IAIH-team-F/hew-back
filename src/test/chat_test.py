import uuid

import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import bodies, tbls, reses
from hew_back.util import keycloak


@pytest_asyncio.fixture
async def post_chat_body(session) -> bodies.PostChatBody:
    uid = "df56c011-8025-468a-a390-202e6f0d6328"
    profile = keycloak.KeycloakUserProfile(
        sub=uid,
        email_verified=True,
        preferred_username="post_chat_body",
        email="post_chat_body@example.com",
    )
    body = bodies.PostUserBody(
        user_name="post_chat_body",
        user_icon_uuid=None,
    )
    await body.save_new(session, profile)
    return bodies.PostChatBody(
        users=[
            uuid.UUID(uid)
        ]
    )


@pytest.mark.asyncio
async def test_post_chat(session, client, registered_token_info, post_chat_body):
    response = await client.post(
        "/api/chat",
        post_chat_body,
        registered_token_info.token
    )
    assert response.status_code == 200, f"invalid status code {response.json()}"
    body = response.json()
    assert body is not None
    chat = reses.ChatRes(**body)

    record = await session.execute(
        sqlalchemy.select(tbls.ChatUserTable)
        .where(tbls.ChatUserTable.chat_id == chat.chat_id)
    )
    user_tbls: list[tbls.ChatUserTable] = record.scalars().all()
    assert len(user_tbls) == len(chat.users)
    for i in range(len(user_tbls)):
        user_tbl = user_tbls[i]
        user_id = chat.users[i]
        assert user_tbl.chat_id == chat.chat_id
        assert user_tbl.user_id == user_id
