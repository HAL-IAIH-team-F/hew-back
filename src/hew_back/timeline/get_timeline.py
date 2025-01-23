from typing import Union

import sqlalchemy
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps, tbls
from hew_back.product.__res import ProductRes
from hew_back.product.product_service import ProductService


class __Service:
    def __init__(
            self,
            session: AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            product_service: ProductService = Depends(),
            limit: int = Query(default=20),
            page: int = Query(default=0),
    ):
        self.__session = session
        self.__user = user
        self.__product_service = product_service
        self.__limit = limit
        self.__page = page

    async def __select_following(self) -> list[tbls.UserFollowTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.UserFollowTable)
            .where(tbls.UserFollowTable.user_id == self.__user.user_table.user_id)
        )
        return [*raw.scalars().all()]

    async def __select_bought(self) -> list[tbls.CartProductTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartProductTable)
            .join(tbls.CartTable)
            .where(sqlalchemy.and_(
                tbls.CartTable.user_id == self.__user.user_table.user_id,
                tbls.CartTable.purchase_date != None,
            ))
        )
        return [*raw.scalars().all()]

    async def __select_bought_creator(self, bought: list[tbls.CartProductTable]) -> list[tbls.CreatorTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorTable)
            .distinct()
            .join(tbls.CreatorProductTable, tbls.CreatorProductTable.creator_id == tbls.CreatorTable.creator_id)
            .where(tbls.CreatorProductTable.product_id.in_([b.product_id for b in bought]))
        )
        return [*raw.scalars().all()]

    async def __select_timeline(
            self, following: list[tbls.UserFollowTable], bought: list[tbls.CartProductTable],
            bought_creator: list[tbls.CreatorTable]
    ) -> list[tbls.ProductTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(
                tbls.ProductTable,
                (
                        sqlalchemy.case((sqlalchemy.not_(tbls.LikeTable.product_id != None), 2), else_=0)
                        + sqlalchemy.case((
                    tbls.CreatorProductTable.creator_id.in_([f.creator_id for f in following]), 2
                ), else_=0)
                        + sqlalchemy.case((
                    tbls.CreatorProductTable.creator_id.in_([f.creator_id for f in bought_creator]), 1
                ), else_=0)
                ).label("point")
            ).distinct()
            .join(tbls.LikeTable, tbls.LikeTable.product_id == tbls.ProductTable.product_id, isouter=True)
            .join(
                tbls.CreatorProductTable, tbls.CreatorProductTable.product_id == tbls.ProductTable.product_id,
                isouter=True
            )
            .where(sqlalchemy.not_(tbls.ProductTable.product_id.in_([b.product_id for b in bought])))
            .order_by("point")
            .limit(self.__limit)
        )
        return [*raw.scalars().all()]

    async def process(self) -> list[ProductRes]:
        following = await self.__select_following()
        bought = await self.__select_bought()
        bought_creator = await self.__select_bought_creator(bought)
        products = await self.__select_timeline(following, bought, bought_creator)
        result = list[ProductRes]()
        for product in products:
            creator_products = await self.__product_service.select_creator_products(product.product_id)
            carts = await self.__product_service.select_cart(product)
            result.append(ProductRes(
                product_id=product.product_id,
                product_price=product.product_price,
                product_title=product.product_title,
                product_thumbnail_uuid=product.product_thumbnail_uuid,
                product_description=product.product_description,
                purchase_date=product.purchase_date,
                creator_ids=[c.creator_id for c in creator_products],
                purchase_info=self.__product_service.new_purchase_info(carts, product),
            ))
        return result


@app.get("/api/timeline")
async def gps(
        service: __Service = Depends(),
) -> list[ProductRes]:
    return await service.process()
