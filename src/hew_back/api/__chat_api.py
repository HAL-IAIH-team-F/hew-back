import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, bodies, deps, reses


@app.post("/api/chat")
async def pc(
        body: bodies.PostChatBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token),
):
    raise NotImplementedError


@app.get("/api/chat/{user_id}")
async def gc(
        user_id: uuid.UUID,
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> list[reses.ChatRes]:
    raise NotImplementedError
