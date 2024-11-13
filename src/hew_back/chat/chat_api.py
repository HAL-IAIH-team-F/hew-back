import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.chat.__body import PostChatBody, PostChatMessageBody
from hew_back.chat.__res import ChatMessageRes, ChatRes


@app.post("/api/chat")
async def pc(
        body: PostChatBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> ChatRes:
    res = await body.save_new(user, session)
    return res.to_chat_res()


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
) -> ChatMessageRes:
    res = await body.save_new(session, chat_id)
    return res.to_chat_message_res()


@app.post("/api/chat/{chat_id}/message")
async def gcms(
        chat_id: uuid.UUID,
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> ChatMessageRes:
    res = await body.save_new(session, chat_id)
    return res.to_chat_message_res()
