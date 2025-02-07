import uuid
from datetime import datetime
from uuid import UUID

import pydantic
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.util.tks import TokenInfo


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
        return await tbls.ProductTable.cart_buy(
            session=session,
            user_id=user_id,
        )


@pydantic.dataclasses.dataclass
class PurchaseInfo:
    content_uuid: uuid.UUID
    token: TokenInfo


@pydantic.dataclasses.dataclass
class ProductRes:
    product_id: uuid.UUID
    product_price: int
    product_title: str
    product_thumbnail_uuid: uuid.UUID
    product_description: str
    purchase_date: datetime
    creator_ids: list[uuid.UUID]
    purchase_info: PurchaseInfo | None = None
