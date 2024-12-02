from datetime import datetime
from typing import Union, List
import uuid

from fastapi import Depends, Query
from hew_back import tbls
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back.recommend import __get
from hew_back import app, deps

from hew_back.recommend.__res import GetRecommendRes
from hew_back.recommend.__get import RecommendGet

# ログインしている状態
@app.get("/recommendation")
async def grly(
        product_id: uuid.UUID,
        session: AsyncSession = Depends(deps.DbDeps.session),
        user: deps.UserDeps = Depends(deps.UserDeps.get),
) -> GetRecommendRes:
    result = await RecommendGet.get_recommend(product_id, session, user)

# ログインしていない状態


