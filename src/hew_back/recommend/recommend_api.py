import uuid
from fastapi import HTTPException

from alembic.util import status
from fastapi import Depends, Query
from typing_extensions import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps

from hew_back.recommend.__res import GetRecommendRes
from hew_back.recommend.__service import RecommendGet, __Service

@app.get("/api/recommend")
async def grly(
        service: __Service = Depends(),
) -> GetRecommendRes: # ←これはlist？
    res = await service.


    res = await RecommendGet.get_recommend()
    if res is None:
        raise ValueError("RecommendResult インスタンスが None です。データが存在しない可能性があります。")
    return res.products_res()
