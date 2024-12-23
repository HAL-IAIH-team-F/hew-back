from fastapi import Depends, Query
from hew_back import app
from hew_back.recommend.__res import GetRecommendRes
from hew_back.recommend.__service import __Service
from hew_back.recommend.__result import RecommendResult


@app.get("/api/recommend")
async def grly(
        service: __Service = Depends(),
) -> list[GetRecommendRes]:
    res_list: list[RecommendResult] = await service.request()
    result = []
    for res in res_list:
        result.extend(res.product_res()) # 各RecommendResultに対して、products_resを呼び出す
    return result
