from sqlalchemy.testing.suite.test_reflection import users

from hew_back.db import BaseTable
from sqlalchemy.ext.asyncio import AsyncSession

import uuid
from typing import Union

from fastapi import Query

from sqlalchemy import Column, UUID, Boolean, ForeignKey, select, update

from hew_back import tables

class ProductCartTable(BaseTable):
    __tablename__ = 'TBL_PRODUCT_CART'

    user_id = Column(UUID(as_uuid=True), ForeignKey('TBL_USER.user_id'), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)
    flag = Column(Boolean, default=True, nullable=False)

    @staticmethod
    async def get_product_cart(
            session: AsyncSession,
            user_id: uuid,
            user_mail: str,
            user_name: str,
    ):
        stmt = (select(tables.ProductTable)
                .where(ProductCartTable.product_id==tables.ProductTable.product_id)
                .where(ProductCartTable.flag.is_(True))
                .where(tables.ProductCartTable.user_id==user_id)
                .where(tables.UserTable.user_mail==user_mail)
                .where(tables.UserTable.user_name==user_name)
                )
        result = await session.execute(stmt)
        product_cart = result.scalars().all()
        return product_cart

    @staticmethod
    async def put_product_cart(
            session: AsyncSession,
            product_id:Union[list[uuid.UUID], None],
            user_id: uuid,
    ):
        stmt = (
            update(tables.ProductCartTable)
            .where(tables.ProductCartTable.product_id.in_(product_id))
            .where(tables.ProductCartTable.user_id==user_id)
            .values(flag=False)
        )
        await session.execute(stmt)
        await session.commit()  # コミットして変更を適用

        return await ProductCartTable.get_product_cart(session, user_id)
