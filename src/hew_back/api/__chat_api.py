import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, bodies, deps, reses


@app.post("/api/chat")
async def pc(
        body: bodies.PostChatBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> reses.ChatRes:
    res = await body.save_new(user, session)
    return res.to_chat_res()


@app.get("/api/chat")
async def gc(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> list[reses.ChatRes]:
    chats = await user.find_chats(session)
    return chats.to_chat_reses()


@app.post("/api/chat/{chat_id}/message")
async def pcm(
        body: bodies.PostChatMessageBody,
        chat_id: uuid.UUID,
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> reses.ChatMessageRes:
    res = await body.save_new(session, chat_id)
    return res.to_chat_message_res()
