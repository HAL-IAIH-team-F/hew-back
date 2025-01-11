import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls
from hew_back.product.__res import PurchaseInfo


class ProductService:
    def __init__(
            self,
            session: AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps | None = Depends(deps.UserDeps.get_or_none),
    ):
        self.__session = session
        self.__user = user

    async def select_cart(self, product: tbls.ProductTable):
        if self.__user is None:
            return None
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartTable)
            .join(tbls.CartProductTable, tbls.CartTable.cart_id == tbls.CartProductTable.cart_id)
            .where(sqlalchemy.and_(
                tbls.CartProductTable.product_id == product.product_id,
                tbls.CartTable.purchase_date != None,
                tbls.CartTable.user_id == self.__user.user_table.user_id,
            ))
        )
        return raw.scalar_one_or_none()

    @staticmethod
    def new_purchase_info(cart: tbls.CartTable | None, product: tbls.ProductTable):
        if cart is None:
            return None
        return PurchaseInfo(
            content_uuid=product.product_contents_uuid,
        )
