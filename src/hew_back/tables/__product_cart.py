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
            session: AsyncSession
    ):
        stmt = (select(tables.ProductTable)
                .where(ProductCartTable.product_id==tables.ProductTable.product_id)
                .where(tables.ProductCartTable.flag.is_(True)))
        result = await session.execute(stmt)
        product_cart = result.scalars().all()
        return product_cart

    @staticmethod
    async def put_product_cart(
            session: AsyncSession,
            product_id :Union[list[uuid.UUID], None] = Query(),
    ):
        stmt = (
            update(tables.ProductCartTable)
            .where(tables.ProductCartTable.product_id.in_(product_id))
            .values(flag=False)
        )
        result = await session.execute(stmt)
        result.scalars().all()
        await session.commit()  # コミットして変更を適用

        return {"message": "Product cart updated successfully"}
