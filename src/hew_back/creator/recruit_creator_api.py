from hew_back import app, deps

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from __res import RecruitCreator

from sqlalchemy.ext.asyncio import AsyncSession

@app.post("/api/recruit_creator_endpoint")
async def recruit_creator_endpoint(
        session: AsyncSession = Depends(deps.DbDeps.session),
        user_deps: deps.UserDeps = Depends(deps.UserDeps.get),
):
    user_id = user_deps.user_table.user_id
    result = await RecruitCreator.recruit_creator(
        session=session,
        user_id=user_id,
    )
