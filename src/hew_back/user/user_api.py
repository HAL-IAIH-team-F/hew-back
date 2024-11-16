from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.user.__res import SelfUserRes
from hew_back.user.__user_body import PostUserBody
from hew_back.util import err


@app.post("/api/user")
async def post_user(
        body: PostUserBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token),
) -> SelfUserRes:
    model = await body.save_new(session, token.profile)
    return model.to_self_user_res()


@app.get("/api/user/self")
async def get_user(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> SelfUserRes:
    if user is None:
        raise err.ErrorIdException(err.ErrorIds.USER_NOT_FOUND)
    return user.to_self_user_res()
