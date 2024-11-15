import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import bodies, tbls, reses
from hew_back.reses import ChatRes


@pytest_asyncio.fixture
async def post_chat_body(session, user_saved) -> bodies.PostChatBody:
    return bodies.PostChatBody(
        users=[
            user_saved.user_id
        ]
    )


@pytest_asyncio.fixture
async def chat_saved(session, user_saved, login_user_deps) -> reses.ChatRes:
    body = bodies.PostChatBody(
        users=[
            user_saved.user_id
        ]
    )
    res = await body.save_new(login_user_deps, session)
    return res.to_chat_res()


@pytest.fixture
def chat_saved_list(chat_saved) -> list[ChatRes]:
    return [chat_saved]


@pytest.mark.asyncio
async def test_post_chat(session, client, login_access_token, post_chat_body):
    response = await client.post(
        "/api/chat",
        post_chat_body,
        login_access_token.token
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


@pytest.mark.asyncio
async def test_get_chat(client, login_access_token, session, chat_saved_list):
    result = await client.get(
        "/api/chat",
        login_access_token.token
    )
    assert result.status_code == 200, f"invalid status code {result.read()}"
    body = result.json()
    assert body is not None
    assert len(chat_saved_list) == len(body)
    for i in range(len(chat_saved_list)):
        chat = chat_saved_list[i]
        res = reses.ChatRes(**body[i])
        assert chat.chat_id == res.chat_id
        for user_i in range(len(chat.users)):
            assert chat.users[user_i] == res.users[user_i]
