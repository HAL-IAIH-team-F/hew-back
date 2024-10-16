from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, bodies, responses, deps
from hew_back.util import err


@app.post("/api/user")
async def post_user(
        body: bodies.PostUserBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token),
) -> responses.SelfUserRes:
    model = await body.save_new(session, token.profile)
    return model.to_self_user_res()


@app.get("/api/user/self")
async def get_user(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> responses.SelfUserRes:
    if user is None:
        raise err.ErrorIdException(err.ErrorIds.USER_NOT_FOUND)
    return user.to_self_user_res()
