import uuid

from sqlalchemy import Column, String, DateTime, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import select, join, or_, func

import datetime
from typing import Union, List

from hew_back import tables
from hew_back.db import BaseTable

import datetime


# from hew_back import table


class ProductTable(BaseTable):
    __tablename__ = 'TBL_PRODUCT'

    product_id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)
    product_price = Column(String(64), nullable=False)
    product_title = Column(String(64), nullable=False)
    product_text = Column(String(255), nullable=False)
    product_date = Column(DateTime, default=datetime.datetime.now)
    product_thumbnail_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    product_contents_uuid = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    @staticmethod
    async def find_products_or_null(
            session: AsyncSession,
            name: Union[List[str], None],
            tag: Union[List[str], None],
            post_by: [List[UUID], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None]
    ):
        # from hew_back.table import ProductTag
        # from hew_back.table import Tag

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
            # メインクエリにサブクエリを結合して、製品をフィルタリング
            stmt = stmt.join(tag_subquery, ProductTable.product_id == tag_subquery.c.product_id)

        if start_datetime is not None:
            start_datetime = start_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.product_date >= start_datetime)

        if end_datetime is not None:
            end_datetime = end_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.product_date <= end_datetime)


        result = await session.execute(stmt)

        products = result.scalars().all()
        return products

        # return query

# # データベースエンジンの作成とテーブルの作成
# from sqlalchemy import create_engine
#
# engine = create_engine('sqlite:///products.db')
# Base.metadata.create_all(engine)
