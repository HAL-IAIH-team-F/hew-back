import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, bodies, deps, reses


@app.post("/api/chat")
async def pc(
        body: bodies.PostChatBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
):
    await body.save_new(user, session)
    return {}


@app.get("/api/chat/{user_id}")
async def gc(
        user_id: uuid.UUID,
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> list[reses.ChatRes]:
    raise NotImplementedError
