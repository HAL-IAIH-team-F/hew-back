from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.creator.__body import PostCreatorBody
from hew_back.creator.__creator_service import CreatorService
from hew_back.creator.__res import CreatorResponse


# FastAPIアプリケーションを作成します


# POSTリクエストを受け取るエンドポイントを定義します
@app.post("/api/creator")
async def pc(
        body: PostCreatorBody,
        user_deps: deps.UserDeps = Depends(deps.UserDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
        creator_service: CreatorService = Depends(),
        user_service: UserService = Depends(),
) -> CreatorResponse:
    result = await body.save_new(user_deps, session)
    return CreatorResponse(
        creator_id=result.creator.creator_id,
        contact_address=result.creator.contact_address,
        user_data=creator_service.create_user_data(await user_service.select_user(result.creator))
    )
