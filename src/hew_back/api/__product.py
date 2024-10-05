from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, models
from hew_back.db import DB

from typing import Union, List
from datetime import datetime

from uuid import UUID



@app.get("/products/")
async def read_products(
        name: Union[List[str], None] = Query(default=None, description="for_0_to_multiple_product_or_tag_name_post_by"),
        tag: Union[List[str], None] = Query(default=None, description="tag_related_product"),
        post_by: Union[List[UUID], None] = Query(default=None, description="created_by"),
        start_datetime: Union[datetime, None] = Query(default=None, description="start_datetime"),
        end_datetime: Union[datetime, None] = Query(default=None, description="end_datetime"),
        following: Union[bool, None] = Query(default=None, description="user_following"), # ← settion通信？してUserテーブルからログインしているユーザーがフォローしているか取ってくるコードが必要なのでは？
        read_limit_number: Union[int, None] = Query(default=None, description="read_product_limit_number"),
        session: AsyncSession = Depends(DB.get_session)
):
    # query_items = {
    #     "name": name,
    #     "start_datetime": start_datetime,
    #     "end_datetime": end_datetime,
    #     "following": following,
    #     "read_limit_number": read_limit_number
    # }

    if start_datetime and end_datetime and start_datetime > end_datetime:
        raise HTTPException(status_code=405, detail="start_datetime cannot be greater than end_datetime")
    product_service = models.GetProductsResponse(session=session)  # インスタンス化
    search_products = await product_service.get_products(
        session=session,
        # self,
        name=name,
        tag=tag,
        post_by=post_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        following=following,
        read_limit_number=read_limit_number
    )
    return search_products




# True
# http://127.0.0.1:8000/products/?name=AdoのTシャツ&start_datetime=2024-01-01T00:00:00Z&end_datetime=2024-01-31T23:59:59Z&read_limit_number=10

# Error
# http://127.0.0.1:8000/products/?name=Ado&name=グッズ&start_datetime=2024-01-31T23:59:59Z&end_datetime=2024-01-01T00:00:00Z

