import uuid

import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps, tbls
from hew_back.product.__res import ProductRes


class __Service:
    def __init__(
            self,
            product_id: uuid.UUID,
            session: AsyncSession = Depends(deps.DbDeps.session)
    ):
        self.__session = session
        self.__product_id = product_id

    async def __select_product(self) -> tbls.ProductTable:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.ProductTable)
            .where(tbls.ProductTable.product_id == self.__product_id)
        )
        return raw.scalar_one()

    async def __select_creator_products(self) -> list[tbls.CreatorProductTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorProductTable)
            .where(tbls.CreatorProductTable.product_id == self.__product_id)
        )
        return [*raw.scalars().all()]

    async def process(self) -> ProductRes:
        product = await self.__select_product()
        creator_products = await self.__select_creator_products()
        return ProductRes(
            product_description=product.product_description,
            product_id=product.product_id,
            product_thumbnail_uuid=product.product_thumbnail_uuid,
            product_price=product.product_price,
            product_title=product.product_title,
            purchase_date=product.purchase_date,
            product_contents_uuid=product.product_contents_uuid,
            creator_ids=[c.creator_id for c in creator_products],
        )


@app.get("/api/product/{product_id}")
async def gp(
        service: __Service = Depends(),
) -> ProductRes:
    return await service.process()
