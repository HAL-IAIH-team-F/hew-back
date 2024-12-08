from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.follow.__body import UserFollow


@app.post("/api/user_follow")
async def cfc(
        body: UserFollow,
        user_deps: deps.UserDeps = Depends(deps.UserDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> None:
    await body.save_new(user_deps, session)
