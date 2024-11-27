from fastapi import Depends

from hew_back import app, deps
from hew_back.user import __post_user
from hew_back.user.__res import SelfUserRes
from hew_back.util import err


@app.post("/api/user")
async def post_user(
        result=Depends(__post_user.post_user),
) -> SelfUserRes:
    return result.to_self_user_res()


@app.get("/api/user/self")
async def get_user(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> SelfUserRes:
    if user is None:
        raise err.ErrorIdException(err.ErrorIds.USER_NOT_FOUND)
    return user.to_self_user_res()
