import pytest
import pytest_asyncio
import sqlalchemy

from hew_back import bodies, tbls, reses
from hew_back.bodies import PostChatMessageBody
from hew_back.reses import ChatRes


@pytest.fixture
def post_chat_body(session, user_saved) -> bodies.PostChatBody:
    return bodies.PostChatBody(
        users=[
            user_saved.user_id
        ]
    )


@pytest.fixture
def post_chat_message_body(session) -> PostChatMessageBody:
    return bodies.PostChatMessageBody(
        message="post_chat_message_body",
        images=[]
    )


@pytest_asyncio.fixture
async def saved_chat(session, user_saved, login_user_deps) -> reses.ChatRes:
    body = bodies.PostChatBody(
        users=[
            user_saved.user_id
        ]
    )
    res = await body.save_new(login_user_deps, session)
    return res.to_chat_res()


@pytest.fixture
def chat_saved_list(saved_chat) -> list[ChatRes]:
    return [saved_chat]


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


@pytest.mark.asyncio
async def test_post_chat(session, client, login_access_token, saved_chat, post_chat_message_body):
    response = await client.post(
        f"/api/chat/{saved_chat.chat_id}/message",
        post_chat_message_body,
        login_access_token.token
    )
    assert response.status_code == 200, f"invalid status code {response.json()}"
    body = response.json()
    assert body is not None
    message = reses.ChatMessageRes(**body)

    result = await session.execute(
        sqlalchemy.select(tbls.ChatMessageTable)
        .where(tbls.ChatMessageTable.chat_message_id == message.chat_message_id)
    )
    record: tbls.ChatMessageTable = result.scalar_one()

    assert record.chat_id == message.chat_id
    assert record.chat_message_id == message.chat_message_id
    assert record.message == message.message
    assert record.index == message.index

    result = await session.execute(
        sqlalchemy.select(tbls.ChatImageTable)
        .where(tbls.ChatImageTable.chat_message_id == record.chat_id)
    )
    image_records: list[tbls.ChatImageTable] = result.scalars().all()

    assert len(image_records) == len(message.images)
    for i in range(len(image_records)):
        image = image_records[i]
        assert image.image_uuid == message.images[i]
