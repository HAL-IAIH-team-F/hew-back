from fastapi import Depends

from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import table, model
from hew_back.db import DB

from typing import Union, List
from datetime import datetime

from uuid import UUID

# import uuid


# 例:文字列のクエリパラメーターを受け取る
# api → model → table
# 最終的にtableでjoin句などを使用して、product_idなどを返し、それをapiに伝える
# table → model → api
class GetProductsResponse(BaseModel):
    # product_id: uuid
    # product_name: str

    @staticmethod
    async def get_products(
        session: AsyncSession,
        name: Union[List[str], None],
        tag: Union[List[str], None],
        post_by: Union[List[UUID], None],
        start_datetime: Union[datetime, None],
        end_datetime: Union[datetime, None],
        following: Union[bool, None],
        read_limit_number: Union[int, None],
    ):
        products_fr_tbl = await table.ProductTable.find_products_or_null(
            session=session,
            name=name,
            tag=tag,
            post_by=post_by,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            following=following,
            read_limit_number=read_limit_number
        )
        return products_fr_tbl,  # name, start_datetime, end_datetime, following, read_limit_number, products_fr_tbl



