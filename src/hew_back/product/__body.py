import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, deps
from hew_back.product.__result import PostCreatorResult


class PostProductBody(BaseModel):
    price: int
    product_title: str
    product_description: str
    listing_date: datetime
    product_thumbnail_uuid: uuid.UUID
    product_contents_uuid: uuid.UUID

    async def save_new(self, creator: deps.CreatorDeps, session: AsyncSession) -> PostCreatorResult:
        product = tbls.ProductTable.insert(
            session,
            product_price=self.price,
            product_title=self.product_title,
            product_description=self.product_description,
            listing_date=self.listing_date,
            product_thumbnail_uuid=self.product_thumbnail_uuid,
            product_contents_uuid=self.product_contents_uuid,
        )
        await session.flush()
        await session.refresh(product)
        creator_product = tbls.CreatorProductTable.insert(
            session, creator.creator_table, product
        )
        await session.flush()
        await session.refresh(creator_product)
        return PostCreatorResult(
            product, creator_product
        )
