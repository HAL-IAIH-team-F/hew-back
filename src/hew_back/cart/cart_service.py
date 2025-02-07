import sqlalchemy
from fastapi import Depends

from hew_back import deps, tbls
from hew_back.util import err


class CartService:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.__session = session
        self.__user = user

    @staticmethod
    def validate_cart_is_not_none(cart: tbls.CartTable):
        if cart is not None:
            return
        raise err.ErrorIds.INTERNAL_ERROR.to_exception("A cart not exists for this user and has not been completed.")

    async def __select_cart(self) -> tbls.CartTable:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartTable)
            .where(sqlalchemy.and_(
                tbls.CartTable.user_id == self.__user.user_table.user_id,
                tbls.CartTable.purchase_date == None,
            ))
        )
        return raw.scalar_one_or_none()

    async def select_or_insert_cart(self) -> tbls.CartTable:
        cart = await self.__select_cart()
        if cart is not None:
            return cart
        cart = tbls.CartTable(
            user_id=self.__user.user_table.user_id,
        )
        self.__session.add(cart)
        await self.__session.flush()
        await self.__session.refresh(cart)
        return cart

    async def select_cart_product(self, cart: tbls.CartTable) -> list[tbls.CartProductTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartProductTable)
            .where(
                tbls.CartProductTable.cart_id == cart.cart_id,
                tbls.CartProductTable.removed == False,
            )
        )
        return [*raw.scalars().all()]
