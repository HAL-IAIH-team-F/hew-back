from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.creator.__body import PostCreatorBody
from hew_back.responses import CreatorResponse


# FastAPIアプリケーションを作成します


# POSTリクエストを受け取るエンドポイントを定義します
@app.post("/api/creator")
async def pc(
        body: PostCreatorBody,
        user_deps: deps.UserDeps = Depends(deps.UserDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> CreatorResponse:
    result = await body.save_new(user_deps, session)
    return result.to_creator_res()
