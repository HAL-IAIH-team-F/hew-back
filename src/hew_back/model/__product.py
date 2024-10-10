# import uuid

from fastapi import Depends

from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import table, model
from hew_back.db import DB

from typing import Union, List
from datetime import datetime

from uuid import UUID

# import uuid

from hew_back.util import OrderDirection


class GetProductsResponse(BaseModel):
    product_text: str
    product_id: UUID
    product_thumbnail_uuid: UUID
    product_price: int
    product_title: str
    product_date: datetime
    product_contents_uuid: UUID



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
        time_order: OrderDirection,
        name_order: OrderDirection,
        like_order: OrderDirection,
        sort: List[str]
    ) -> List["GetProductsResponse"]:
        products_data = await table.ProductTable.find_products_or_null(
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
            sort=sort,
        )



        # Pydanticモデルのリストに変換

        # **は辞書の展開を意味
        # product.__dict__に含まれるキーと値が、GetProductsResponseのフィールドにマッピング
        if products_data:
            return [GetProductsResponse(**product.__dict__) for product in products_data]
        else:
            return []

    class Config:
        from_attributes = True  # SQLAlchemyオブジェクトからPydanticモデルへの変換を有効に


