from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, model, error
from hew_back.db import DB


@app.post("/api/user")
async def post_user(
        body: model.PostUserBody,
        session: AsyncSession = Depends(DB.get_session),
        token: model.JwtTokenData = Depends(model.JwtTokenData.get_access_token_or_none),
) -> model.SelfUserRes:
    return await  body.to_self_user_res(session, token.profile)


@app.get("/api/user/self")
async def get_user(
        user: model.SelfUserRes = Depends(model.SelfUserRes.get_self_user_res_or_none),
) -> model.SelfUserRes:
    if user is None:
        raise error.ErrorIdException(model.ErrorIds.USER_NOT_FOUND)
    return user
