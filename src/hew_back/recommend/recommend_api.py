import uuid

from fastapi import Depends, Query
from typing_extensions import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from hew_back.recommend import __service
from hew_back import app, deps

from hew_back.recommend.__res import GetRecommendRes
from hew_back.recommend.__service import RecommendGet

# ログインしている状態

@app.get("/api/recommend")
async def grly(
        session: AsyncSession = Depends(deps.DbDeps.session),
        user_deps: Optional[deps.UserDeps] = Depends(deps.UserDeps.get_or_none),
        size: int = Query(None, ge=20, le=30),
        product_id: uuid.UUID = Query(),
        user_id: uuid.UUID = Query(),
) -> GetRecommendRes:
    res = await RecommendGet.get_recommend(session, user_deps, size, product_id, user_id)
    return res.products_res()

