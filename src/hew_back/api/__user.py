from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, model
from hew_back.db import DB


@app.post("/api/user")
async def post_user(
        body: model.PostUserBody,
        session: AsyncSession = Depends(DB.get_session),
        token: model.JwtTokenData = Depends(model.JwtTokenData.get_access_token_or_none),
) -> model.UserRes:
    user_tbl = body.new_record(session, token.profile)
    await session.commit()
    await session.refresh(user_tbl)
    return model.UserRes.create_by_user_table( user_tbl)
