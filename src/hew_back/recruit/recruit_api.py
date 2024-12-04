from datetime import datetime
from typing import Union

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps
from hew_back.recruit.__post_recruit import post_recruit
from hew_back.recruit.__reses import RecruitRes
from hew_back.util import OrderDirection
from hew_back.util.err import ErrorIds


@app.post("/api/recruit")
async def pr(
        response: RecruitRes = Depends(post_recruit),
) -> RecruitRes:
    return response


@app.get("/api/recruit")
async def grs(
        name: Union[list[str], None] = Query(default=None),
        tag: Union[list[str], None] = Query(default=None),
        post_by: Union[list[str], None] = Query(default=None),
        start_datetime: Union[datetime, None] = Query(default=None),
        end_datetime: Union[datetime, None] = Query(default=None),
        following: Union[bool, None] = Query(default=None),
        limit: Union[int, None] = Query(default=20),
        time_order: OrderDirection = Query(default=None),
        name_order: OrderDirection = Query(default=None),
        like_order: OrderDirection = Query(default=None),
        sort: list[str] = Query(default=None),
        session: AsyncSession = Depends(deps.DbDeps.session)
) -> list[RecruitRes]:
    if start_datetime and end_datetime and start_datetime > end_datetime:
        raise ErrorIds.DATETIME_CONFLICT.to_exception( "start_datetime cannot be greater than end_datetime")

    search_products = await ProductFinder.find_products(
        session=session,
        name=name,
        tag=tag,
        post_by=post_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        following=following,
        read_limit_number=limit,
        time_order=time_order,
        name_order=name_order,
        like_order=like_order,
        sort=sort
    )
    return search_products.to_get_products_res()
