from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, model, error
from hew_back.db import DB

from typing import Union, List
from datetime import datetime

from uuid import UUID



@app.get("/products/")
async def read_products(
        q: Union[List[str], None] = Query(default=None, description="for_0_to_multiple_product_or_tag_name_post_by"),
        post_by: Union[List[UUID], None] = Query(default=None, description="created_by"),
        start_datetime: Union[datetime, None] = Query(default=None, description="start_datetime"),
        end_datetime: Union[datetime, None] = Query(default=None, description="end_datetime"),
        following: Union[bool, None] = Query(default=None, description="user_following"), # ← settion通信？してUserテーブルからログインしているユーザーがフォローしているか取ってくるコードが必要なのでは？
        read_limit_number: Union[int, None] = Query(default=None, description="read_product_limit_number"),
        # TODO  ASK: この時点でDB.get_settionを実行して、AsyncSettionを生成し、データベース操作を行えるようにする必要があるのだろうか？
        session: AsyncSession = Depends(DB.get_session)
):
    # query_items = {
    #     "name": q,
    #     "start_datetime": start_datetime,
    #     "end_datetime": end_datetime,
    #     "following": following,
    #     "read_limit_number": read_limit_number
    # }

    if start_datetime and end_datetime and start_datetime > end_datetime:
        raise HTTPException(status_code=405, detail="start_datetime cannot be greater than end_datetime")

    # 検索履歴残したり今後のことを考えてインスタンス化　→　modelでは@staticmethodは使用しない
    product_service = model.GetProductsResponse(session=session)  # インスタンス化
    search_products = await product_service.get_products(
        session=session,
        # self,
        q=q,
        post_by=post_by,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        following=following,
        read_limit_number=read_limit_number
    )

    return search_products




# True
# http://127.0.0.1:8000/products/?q=AdoのTシャツ&start_datetime=2024-01-01T00:00:00Z&end_datetime=2024-01-31T23:59:59Z&read_limit_number=10

# Error
# http://127.0.0.1:8000/products/?q=Ado&q=グッズ&start_datetime=2024-01-31T23:59:59Z&end_datetime=2024-01-01T00:00:00Z

