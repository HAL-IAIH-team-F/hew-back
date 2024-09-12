import uuid

from sqlalchemy import Column,  String, DateTime, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
# from asyncpg.pgproto.pgproto import UUID
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import select, join, or_

import datetime
from typing import Union, List

from hew_back.db import BaseTable
from hew_back import table

# from uuid import UUID



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
            q: Union[List[str], None],
            post_by: [List[UUID], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None]
    ):
        # from hew_back.table import ProductTag
        # from hew_back.table import Tag
        stmt = (
            select(ProductTable)
            # .select_from(
            #     join(ProductTable, table.ProductTag, ProductTable.product_id == table.ProductTag.item_id)
            #     .join(table.Tag, table.ProductTag.tag_id == table.Tag.tag_id)
            # )
            .where(
                # table.Tag.tag_name.in_(q)
                or_(*[ProductTable.product_title.like(f"{keyword}") for keyword in q])
            )
        )

        result = await session.execute(stmt)

        products = result.scalars().all()
        return products






        # return query





# # データベースエンジンの作成とテーブルの作成
# from sqlalchemy import create_engine
#
# engine = create_engine('sqlite:///products.db')
# Base.metadata.create_all(engine)
