import uuid
from datetime import datetime
from typing import Union

import pydantic.dataclasses
import sqlalchemy
from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, app, tbls
from hew_back.product.__res import ProductRes
from hew_back.product.product_service import ProductService
from hew_back.tbls import CreatorProductTable
from hew_back.util import OrderDirection


@pydantic.dataclasses.dataclass
class PostCollaboApproveBody:
    collabo_id: uuid.UUID


class __Service:
    def __init__(
            self,
            name: Union[list[str], None] = Query(default=None,
                                                 description="for_0_to_multiple_product_or_tag_name_post_by"),
            tag: Union[list[str], None] = Query(default=None, description="tag_related_product"),
            post_by: Union[list[str], None] = Query(default=None, description="created_by"),
            start_datetime: Union[datetime, None] = Query(default=None, description="start_datetime"),
            end_datetime: Union[datetime, None] = Query(default=None, description="end_datetime"),
            following: Union[bool, None] = Query(default=None, description="user_following"),
            limit: Union[int, None] = Query(default=20, description="read_product_limit_number"),
            time_order: OrderDirection = Query(default=None, description="time_direction asc/desc"),
            name_order: OrderDirection = Query(default=None, description="name_direction asc/desc"),
            like_order: OrderDirection = Query(default=None, description="like_direction asc/desc"),
            sort: list[str] = Query(
                default=None,
                description="List may be included datetime or name or like,witch is gaven default asc or desc"
            ),
            session: AsyncSession = Depends(deps.DbDeps.session),
            product_service: ProductService = Depends(),
    ):
        if start_datetime and end_datetime and start_datetime > end_datetime:
            raise HTTPException(status_code=400, detail="start_datetime cannot be greater than end_datetime")
        self.product_service = product_service
        self.session = session
        self.name = name
        self.tag = tag
        self.post_by = post_by
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.following = following
        self.limit = limit
        self.time_order = time_order
        self.name_order = name_order
        self.like_order = like_order
        self.sort = sort

    async def name_query(
            self, where: list[sqlalchemy.ColumnElement[bool]]
    ):
        if self.name is not None and len(self.name) > 0:
            where.append(
                sqlalchemy.and_(*[
                    tbls.ProductTable.product_title.like(f"%{keyword}%") for keyword in self.name
                ])
            )

    async def start_datetime_query(
            self, where: list[sqlalchemy.ColumnElement[bool]]
    ):
        if self.start_datetime is not None:
            start_datetime = self.start_datetime.replace(tzinfo=None)
            where.append(tbls.ProductTable.purchase_date >= start_datetime)

    async def end_datetime_query(
            self, where: list[sqlalchemy.ColumnElement[bool]]
    ):
        if self.end_datetime is not None:
            end_datetime = self.end_datetime.replace(tzinfo=None)
            where.append(tbls.ProductTable.purchase_date <= end_datetime)

    async def tag_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.tag is not None and len(self.tag) > 0:
            tag_subquery = (
                sqlalchemy.select(
                    tbls.ProductTag.item_id.label("product_id")
                )
                .join(tbls.Tag, tbls.ProductTag.tag_id == tbls.Tag.tag_id)
                .where(tbls.Tag.tag_name.in_(self.tag))
                # ProductTag.item_idをgroup_byすることで、ProductTag テーブルの item_id（製品ID）ごとにグループ化
                # →中間テーブルの特性上、その製品に関連付けられたタグ情報がまとめられる
                .group_by(tbls.ProductTag.item_id)
                # 各 item_id に関連するタグの数が指定した条件と一致したら
                .having(sqlalchemy.func.count(tbls.ProductTag.tag_id) == len(self.tag))
                .subquery()
            )
            # メインクエリにサブクエリを結合して、製品をフィルタリングしています
            stmt = stmt.join(tag_subquery, tbls.ProductTable.product_id == tag_subquery.c.product_id)
        return stmt

    async def post_by_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.post_by is not None and len(self.post_by) > 0:
            post_by_subquery = (
                sqlalchemy.select(
                    tbls.CreatorProductTable.product_id.label("product_id")
                )
                .join(tbls.CreatorTable, tbls.CreatorProductTable.creator_id == tbls.CreatorTable.creator_id)
                .join(tbls.UserTable, tbls.UserTable.user_id == tbls.CreatorTable.user_id)
                .where(tbls.UserTable.user_name.in_(self.post_by))
                .group_by(tbls.CreatorProductTable.product_id)
                .having(sqlalchemy.func.count(tbls.UserTable.user_name) == len(self.post_by))
                .subquery()
            )
            stmt = stmt.join(post_by_subquery, tbls.ProductTable.product_id == post_by_subquery.c.product_id)

        return stmt

    async def following_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.following:
            following_subquery = (
                sqlalchemy.select(
                    tbls.UserFollowTable.creator_id
                )
                .subquery()
            )
            stmt = (
                sqlalchemy.select(tbls.ProductTable)
                .join(tbls.CreatorProductTable, tbls.ProductTable.product_id == tbls.CreatorProductTable.product_id)
                .join(tbls.CreatorTable, tbls.CreatorProductTable.creator_id == tbls.CreatorTable.creator_id)
                .where(tbls.CreatorProductTable.creator_id.in_(following_subquery))
            )

        return stmt

    async def limit_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.limit is not None and self.limit > 0:
            stmt = stmt.limit(self.limit)
        return stmt

    async def time_order_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.time_order == OrderDirection.ASC:
            stmt = stmt.order_by(tbls.ProductTable.purchase_date.asc())
        elif self.time_order == OrderDirection.DESC:
            stmt = stmt.order_by(tbls.ProductTable.purchase_date.desc())
        return stmt

    async def name_order_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        if self.name_order == OrderDirection.ASC:
            stmt = stmt.order_by(tbls.ProductTable.product_title.asc())
        elif self.name_order == OrderDirection.DESC:
            stmt = stmt.order_by(tbls.ProductTable.product_title.desc())
        return stmt

    async def likes_query(
            self, stmt: sqlalchemy.Select[tuple[tbls.ProductTable]]
    ) -> sqlalchemy.Select[tuple[tbls.ProductTable]]:
        likes_subquery = (
            sqlalchemy.select(
                tbls.LikeTable.product_id,
                sqlalchemy.func.count(tbls.LikeTable.product_id).label("like_count")
            )
            .group_by(tbls.LikeTable.product_id)
            .subquery()
        )
        stmt = stmt.outerjoin(likes_subquery, tbls.ProductTable.product_id == likes_subquery.c.product_id)
        if self.like_order == OrderDirection.ASC:
            stmt = stmt.order_by(likes_subquery.c.like_count.asc().nullsfirst())
        else:
            stmt = stmt.order_by(likes_subquery.c.like_count.desc().nullslast())

        return stmt

    async def select_products(
            self,
    ) -> list[tbls.ProductTable]:
        stmt = sqlalchemy.select(tbls.ProductTable)
        where = list[sqlalchemy.ColumnElement[bool]]()
        await self.name_query(where)
        stmt = await self.tag_query(stmt)
        stmt = await self.post_by_query(stmt)
        stmt = await self.following_query(stmt)
        await self.start_datetime_query(where)
        await self.end_datetime_query(where)
        stmt = stmt.where(*where)
        stmt = await self.limit_query(stmt)
        stmt = await self.time_order_query(stmt)
        stmt = await self.name_order_query(stmt)
        stmt = await self.likes_query(stmt)

        result = await self.session.execute(stmt)

        products = result.scalars().all()

        return [product for product in products]

    async def select_creator_products(
            self, product: tbls.ProductTable
    ) -> list[CreatorProductTable]:
        records = await self.session.execute(
            sqlalchemy.select(tbls.CreatorProductTable)
            .where(tbls.CreatorProductTable.product_id == product.product_id)
        )
        records = records.scalars().all()
        return [creator_product for creator_product in records]

    async def creator_ids(self, product: tbls.ProductTable) -> list[uuid.UUID]:
        creator_products = await self.select_creator_products(product)
        return [creator_product.creator_id for creator_product in creator_products]

    async def response(self) -> list[ProductRes]:
        products = await self.select_products()
        result = list[ProductRes]()

        for product in products:
            carts = await self.product_service.select_cart(product)
            result.append(ProductRes(
                product_description=product.product_description,
                product_id=product.product_id,
                product_thumbnail_uuid=product.product_thumbnail_uuid,
                product_price=product.product_price,
                product_title=product.product_title,
                purchase_date=product.purchase_date,
                creator_ids=await self.creator_ids(product),
                purchase_info=ProductService.new_purchase_info(carts, product),
            ))
        return result


@app.get("/api/product")
async def gps(
        service: __Service = Depends(),
) -> list[ProductRes]:
    return await service.response()
