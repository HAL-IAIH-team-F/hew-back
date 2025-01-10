import uuid
from datetime import datetime
from uuid import UUID

import pydantic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.tbls import ProductTable


class CartProduct(BaseModel):
    product_id: UUID
    product_price: int
    product_title: str
    product_text: str
    product_date: datetime
    product_contents_uuid: UUID
    product_thumbnail_uuid: UUID

    @staticmethod
    async def cart_buy(
            session: AsyncSession,
            user_id: tbls.UserTable.user_id
    ) -> "ProductTable":
        cart_buy = await tbls.ProductTable.cart_buy(
            session=session,
            user_id=user_id,
        )
        return cart_buy


@pydantic.dataclasses.dataclass
class ProductRes:
    product_description: str
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID
    product_price: int
    product_title: str
    purchase_date: datetime
    product_contents_uuid: uuid.UUID
    creator_ids: list[uuid.UUID]
