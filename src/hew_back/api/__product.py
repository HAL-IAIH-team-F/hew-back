from datetime import datetime
from typing import Union, List

from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, responses, deps
from hew_back.util import OrderDirection


@app.get("/products/")
async def read_products(
        name: Union[List[str], None] = Query(default=None, description="for_0_to_multiple_product_or_tag_name_post_by"),
        tag: Union[List[str], None] = Query(default=None, description="tag_related_product"),
        post_by: Union[List[str], None] = Query(default=None, description="created_by"),
        start_datetime: Union[datetime, None] = Query(default=None, description="start_datetime"),
        end_datetime: Union[datetime, None] = Query(default=None, description="end_datetime"),
        following: Union[bool, None] = Query(default=None, description="user_following"),
        # ← settion通信？してUserテーブルからログインしているユーザーがフォローしているか取ってくるコードが必要なのでは？
        read_limit_number: Union[int, None] = Query(default=20, description="read_product_limit_number"),
        time_order: OrderDirection = Query(default=None, description="time_direction asc/desc"),
        name_order: OrderDirection = Query(default=None, description="name_direction asc/desc"),
        like_order: OrderDirection = Query(default=None, description="like_direction asc/desc"),
        sort: List[str] = Query(
            default=None,
            description="List may be included datetime or name or like,witch is gaven default asc or desc"
        ),
        session: AsyncSession = Depends(deps.DbDeps.session)
):
    # order_by: Literal["created_at", "updated_at"] = "created_at"とできることを後で知ったが、実装した後になって修正するのはめんどくさい

    # query_items = {
    #     "name": name,
    #     "start_datetime": start_datetime,
    #     "end_datetime": end_datetime,
    #     "following": following,
    #     "read_limit_number": read_limit_number
    # }

    if start_datetime and end_datetime and start_datetime > end_datetime:
        raise HTTPException(status_code=400, detail="start_datetime cannot be greater than end_datetime")

    # if isinstance(time_order, list):
    #     raise HTTPException(status_code=400, detail="time_order should be specified only once.")

    search_products = await responses.GetProductsResponse.get_products(
        session=session,
        name=name,
        tag=tag,
        post_by=post_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        following=following,
        read_limit_number=read_limit_number,
        time_order=time_order,
        name_order=name_order,
        like_order=like_order,
        sort=sort
    )
    return search_products

# True
# http://127.0.0.1:8000/products/?name=AdoのTシャツ&start_datetime=2024-01-01T00:00:00Z&end_datetime=2024-01-31T23:59:59Z&read_limit_number=10

# Error
# http://127.0.0.1:8000/products/?name=Ado&name=グッズ&start_datetime=2024-01-31T23:59:59Z&end_datetime=2024-01-01T00:00:00Z
