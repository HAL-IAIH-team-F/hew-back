import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.chat.__body import PostChatMessageBody
from hew_back.chat.__finder import ChatFinder
from hew_back.chat.__res import ChatRes, ChatMessagesRes, MessageRes
from hew_back.chat.chat_service import ChatService


@app.get("/api/chat")
async def gcs(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> list[ChatRes]:
    chats = await user.find_chats(session)
    return chats.to_chat_reses()


@app.post("/api/chat/{chat_id}/message")
async def pcm(
        body: PostChatMessageBody,
        chat_id: uuid.UUID,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> MessageRes:
    res = await body.save_new(session, chat_id, user)
    images: list[uuid.UUID] = []
    for image in res.images:
        images.append(image.image_uuid)
    return ChatService.create_message_res(
        res.message,
        images,
    )


@app.get("/api/chat/{chat_id}/message")
async def gcms(
        chat_id: uuid.UUID,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> ChatMessagesRes:
    res = await ChatFinder.find_chat_messages(session, chat_id, user)
    messages: list[MessageRes] = []
    for message in res.messages:
        images: list[uuid.UUID] = []
        for image in message.images:
            images.append(image.image_uuid)
        messages.append(
            ChatService.create_message_res(
                message.message,
                images,
            ))
    return ChatMessagesRes.create(
        res.chat.chat_id,
        messages
    )
