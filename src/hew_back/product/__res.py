import uuid
from datetime import datetime
from uuid import UUID

import pydantic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls


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
    ):
        await tbls.ProductTable.cart_buy(
            session=session,
            user_id=user_id,
        )


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
