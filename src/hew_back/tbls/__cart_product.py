
from hew_back.db import BaseTable
from sqlalchemy.ext.asyncio import AsyncSession

import uuid



from sqlalchemy import Column, UUID, ForeignKey, select, update

from datetime import datetime

from hew_back import tbls

from zoneinfo import ZoneInfo




class CartProductTable(BaseTable):
    __tablename__ = 'TBL_CART_PRODUCT'

    cart_id = Column(UUID(as_uuid=True), ForeignKey('TBL_CART.cart_id'), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('TBL_PRODUCT.product_id'), primary_key=True)

    @staticmethod
    async def get_cart_products(
            session: AsyncSession,
            user_id: uuid.UUID,
    ):
        # 該当するユーザー
        stmt = (
            select(tbls.ProductTable)
            .join(tbls.CartProductTable, tbls.ProductTable.product_id == tbls.CartProductTable.product_id)
            .join(tbls.CartTable, tbls.CartProductTable.cart_id == tbls.CartTable.cart_id)
            .where(tbls.CartTable.user_id == user_id)
            .where(tbls.CartTable.purchase_date == None)
        )
        result = await session.execute(stmt)
        product_cart = result.scalars().all()
        return product_cart

    @staticmethod
    async def cart_buy(
        session: AsyncSession,
        user_id: uuid.UUID,
    ):
        subquery = (
            select(tbls.CartTable.cart_id)
            .where(tbls.CartTable.user_id == user_id)
            .where(tbls.CartTable.purchase_date == None)
        )

        stmt = (
            update(tbls.CartTable)
            .where(tbls.CartTable.cart_id.in_(subquery))
            .values(purchase_date=datetime.now(ZoneInfo("Asia/Tokyo")).replace(tzinfo=None))
        )


        await session.execute(stmt)
        await session.commit()  # コミットして変更を適用

        return await CartProductTable.get_cart_products(session, user_id)
