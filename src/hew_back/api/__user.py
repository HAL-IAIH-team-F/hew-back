from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, models, bodies, responses
from hew_back.db import DB
from hew_back.util import err


@app.post("/api/user")
async def post_user(
        body: bodies.PostUserBody,
        session: AsyncSession = Depends(DB.get_session),
        token: models.JwtTokenData = Depends(models.JwtTokenData.get_access_token_or_none),
) -> responses.SelfUserRes:
    model = await body.save_new(session, token.profile)
    return model.to_self_user_res()


@app.get("/api/user/self")
async def get_user(
        user: responses.SelfUserRes = Depends(responses.SelfUserRes.get_self_user_res_or_none),
) -> responses.SelfUserRes:
    if user is None:
        raise err.ErrorIdException(err.ErrorIds.USER_NOT_FOUND)
    return user
