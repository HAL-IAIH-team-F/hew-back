import datetime
import uuid
from typing import Union, List

import sqlalchemy
from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tables
from hew_back.db import BaseTable
from hew_back.util import OrderDirection


# from asyncpg.pgproto.pgproto import UUID


# from hew_back import table


class ProductTable(BaseTable):
    __tablename__ = 'TBL_PRODUCT'

    product_id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)
    product_price = Column(sqlalchemy.Integer, nullable=False)
    product_title = Column(String(64), nullable=False)
    product_text = Column(String(255), nullable=False)
    product_date = Column(DateTime, default=datetime.datetime.now)
    product_thumbnail_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    product_contents_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    @staticmethod
    def insert(
            session: AsyncSession,
            product_price: int,
            product_title: str,
            product_text: str,
            product_date: datetime.datetime,
            product_thumbnail_uuid: uuid.UUID,
            product_contents_uuid: uuid.UUID,
    ) -> 'ProductTable':
        table = ProductTable(
            product_price=product_price,
            product_title=product_title,
            product_text=product_text,
            product_date=product_date,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_contents_uuid=product_contents_uuid,
        )
        session.add(table)
        return table

    @staticmethod
    async def find_products_or_null(
            session: AsyncSession,
            name: Union[List[str], None],
            tag: Union[List[str], None],
            post_by: Union[List[str], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None],
            time_order: OrderDirection,
            name_order: OrderDirection,
            like_order: OrderDirection,
            sort: List[str]
    ):
        stmt = select(ProductTable)

        if name is not None and len(name) > 0:
            stmt = stmt.where(
                or_(*[ProductTable.product_title.like(f"%{keyword}%") for keyword in name])
            )

        if tag is not None and len(tag) > 0:
            tag_subquery = (
                select(
                    tables.ProductTag.item_id.label("product_id")
                )
                .join(tables.Tag, tables.ProductTag.tag_id == tables.Tag.tag_id)
                .where(tables.Tag.tag_name.in_(tag))
                # ProductTag.item_idをgroup_byすることで、ProductTag テーブルの item_id（製品ID）ごとにグループ化
                # →中間テーブルの特性上、その製品に関連付けられたタグ情報がまとめられる
                .group_by(tables.ProductTag.item_id)
                # 各 item_id に関連するタグの数が指定した条件と一致したら
                .having(func.count(tables.ProductTag.tag_id) == len(tag))
                .subquery()
            )
            # メインクエリにサブクエリを結合して、製品をフィルタリングしています
            stmt = stmt.join(tag_subquery, ProductTable.product_id == tag_subquery.c.product_id)

        if start_datetime is not None:
            start_datetime = start_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.product_date >= start_datetime)

        if end_datetime is not None:
            end_datetime = end_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.product_date <= end_datetime)

        if post_by is not None and len(post_by) > 0:
            post_by_subquery = (
                select(
                    tables.CreatorProductTable.product_id.label("product_id")
                )
                .join(tables.CreatorTable, tables.CreatorProductTable.creator_id == tables.CreatorTable.creator_id)
                .join(tables.UserTable, tables.UserTable.user_id == tables.CreatorTable.user_id)
                .where(tables.UserTable.user_name.in_(post_by))
                .group_by(tables.CreatorProductTable.product_id)
                .having(func.count(tables.UserTable.user_name) == len(post_by))
                .subquery()
            )
            stmt = stmt.join(post_by_subquery, ProductTable.product_id == post_by_subquery.c.product_id)

        # ログイン機能を作らないときのAPIは役に立ちません　→　ログイン機能作ったら、where句追加してください
        if following:
            following_subquery = (
                select(
                    tables.UserFollowTable.creator_id
                )
                # .where(UserFollowTable.user_id == current_user.user_id) ←　ログイン機能実装後、ログインしているユーザーがフォローしているクリエイターのフィルタリングを行う処理をwhere句で実施していきたい
                .subquery()
            )
            stmt = (
                select(ProductTable)
                .join(tables.CreatorProductTable, ProductTable.product_id == tables.CreatorProductTable.product_id)
                .join(tables.CreatorTable, tables.CreatorProductTable.creator_id == tables.CreatorTable.creator_id)
                .where(tables.CreatorProductTable.creator_id.in_(following_subquery))
            )

        if read_limit_number is not None and read_limit_number > 0:
            stmt = stmt.limit(read_limit_number)

        # time_order に基づいて product_date のソートを追加
        if time_order == OrderDirection.ASC:
            stmt = stmt.order_by(ProductTable.product_date.asc())
        elif time_order == OrderDirection.DESC:
            stmt = stmt.order_by(ProductTable.product_date.desc())
        #
        # name_order に基づいて product_title のソートを追加
        if name_order == OrderDirection.ASC:
            stmt = stmt.order_by(ProductTable.product_title.asc())
        elif name_order == OrderDirection.DESC:
            stmt = stmt.order_by(ProductTable.product_title.desc())

        likes_subquery = (
            select(
                tables.LikeTable.product_id,
                func.count(tables.LikeTable.product_id).label("like_count")
            )
            .group_by(tables.LikeTable.product_id)
            .subquery()
        )
        stmt = stmt.outerjoin(likes_subquery, ProductTable.product_id == likes_subquery.c.product_id)

        if like_order == OrderDirection.ASC:
            stmt = stmt.order_by(likes_subquery.c.like_count.asc().nullsfirst())
        else:
            stmt = stmt.order_by(likes_subquery.c.like_count.desc().nullslast())

        if sort:
            print(sort)
            for sort_field in sort:
                print(sort_field)
                if sort_field == "datetime":
                    stmt = stmt.order_by(ProductTable.product_date.desc())  # datetime のデフォルトは降順
                elif sort_field == "name":
                    stmt = stmt.order_by(ProductTable.product_title.asc())  # name のデフォルトは昇順
                elif sort_field == "like":
                    stmt = stmt.order_by(likes_subquery.c.like_count.desc().nullslast())  # like のデフォルトは降順

        result = await session.execute(stmt)

        products = result.scalars().all()

        return products

        # return query

# # データベースエンジンの作成とテーブルの作成
# from sqlalchemy import create_engine
#
# engine = create_engine('sqlite:///products.db')
# Base.metadata.create_all(engine)
