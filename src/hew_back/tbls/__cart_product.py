
from hew_back.db import BaseTable
from sqlalchemy.ext.asyncio import AsyncSession

import uuid



from sqlalchemy import Column, UUID, ForeignKey, select, update

from datetime import datetime

from hew_back import tables

from zoneinfo import ZoneInfo




class CartProductTable(BaseTable):
    __tablename__ = 'TBL_CART_PRODUCT'

    cart_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CART.cart_id'), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)

    @staticmethod
    async def get_cart_product(
            session: AsyncSession,
            user_id: uuid.UUID,
    ):
        # 該当するユーザー
        stmt = (
            select(tables.ProductTable)
            .join(tables.CartProductTable, tables.ProductTable.product_id == tables.CartProductTable.product_id)
            .join(tables.CartTable, tables.CartProductTable.cart_id == tables.CartTable.cart_id)
            .where(tables.CartTable.user_id == user_id)
            .where(tables.CartTable.purchase_date == None)
        )
        result = await session.execute(stmt)
        product_cart = result.scalars().all()
        return product_cart

    @staticmethod
    async def put_cart_product(
        session: AsyncSession,
        user_id: uuid.UUID,
    ):
        subquery = (
            select(tables.CartTable.cart_id)
            .where(tables.CartTable.user_id == user_id)
            .where(tables.CartTable.purchase_date == None)
        )

        stmt = (
            update(tables.CartTable)
            .where(tables.CartTable.cart_id.in_(subquery))
            .values(purchase_date=datetime.now(ZoneInfo("Asia/Tokyo")).replace(tzinfo=None))
        )


        await session.execute(stmt)
        await session.commit()  # コミットして変更を適用

        return await CartProductTable.get_cart_product(session, user_id)
