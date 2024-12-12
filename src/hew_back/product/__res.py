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
    async def get_cart_product(
            session: AsyncSession,
            user_id: tbls.UserTable.user_id,
    ) -> list["ProductTable"]:
        get_product_cart = await tbls.ProductTable.get_cart_products(
            session=session,
            user_id=user_id,
        )
        return get_product_cart

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
class GetProductsResponse:
    product_description: str
    product_id: uuid.UUID
    product_thumbnail_uuid: uuid.UUID
    product_price: int
    product_title: str
    purchase_date: datetime
    product_contents_uuid: uuid.UUID
    creator_ids: list[uuid.UUID]


class ProductRes(BaseModel):
    product_id: uuid.UUID
    product_price: int
    product_title: str
    product_description: str
    listing_date: datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID
    creator_id: uuid.UUID

    @staticmethod
    def create(
            product_id: uuid.UUID,
            product_price: int,
            product_title: str,
            product_description: str,
            listing_date: datetime,
            product_thumbnail_uuid: uuid.UUID,
            product_contents_uuid: uuid.UUID,
            creator_id: uuid.UUID,
    ):
        return ProductRes(
            product_id=product_id,
            product_price=product_price,
            product_title=product_title,
            product_description=product_description,
            listing_date=listing_date,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_contents_uuid=product_contents_uuid,
            creator_id=creator_id,
        )
