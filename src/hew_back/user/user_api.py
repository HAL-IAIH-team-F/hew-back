from fastapi import Depends

from hew_back import app, deps
from hew_back.creator.__creator_service import CreatorService
from hew_back.user import __post_user
from hew_back.user.__res import SelfUserRes
from hew_back.user.__user_service import UserService
from hew_back.util import err


@app.post("/api/user")
async def post_user(
        result=Depends(__post_user.post_user),
) -> SelfUserRes:
    return result


@app.get("/api/user/self")
async def get_user(
        user: deps.UserDeps = Depends(deps.UserDeps.get),
        creator: deps.CreatorOrNoneDeps = Depends(),
) -> SelfUserRes:
    if user is None:
        raise err.ErrorIdException(err.ErrorIds.USER_NOT_FOUND)
    return UserService.create_user_res(
        user.user_table,
        CreatorService.create_creator_data(creator.creator_table)
    )
