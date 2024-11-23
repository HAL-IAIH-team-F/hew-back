import uuid
from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, deps
from hew_back.chat.__result import MessageResult, ChatMessagesResult
from hew_back.product.__result import ProductsResult
from hew_back.util import OrderDirection


class ProductFinder:
    @staticmethod
    async def find_products(
            session: AsyncSession,
            name: Union[list[str], None],
            tag: Union[list[str], None],
            post_by: Union[list[uuid.UUID], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None],
            time_order: OrderDirection,
            name_order: OrderDirection,
            like_order: OrderDirection,
            sort: list[str]
    ) -> ProductsResult:

        products = await tbls.ProductTable.find_products_or_null(
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
        return ProductsResult(
            products
        )
