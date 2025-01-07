import fastapi
import sqlalchemy
from fastapi import Depends

from hew_back import deps, app, tbls
from hew_back.cart.__reses import CartRes
from hew_back.cart.cart_service import CartService


class __Service:
    def __init__(
            self,
            response: fastapi.Response,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            cart_service: CartService = Depends(),
    ):
        self.__session = session
        self.__user = user
        self.__response = response
        self.__cart_service = cart_service

    async def __select_cart_product(self, cart: tbls.CartTable) -> list[tbls.CartProductTable]:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartProductTable)
            .where(tbls.CartProductTable.cart_id == cart.cart_id)
        )
        return [*raw.scalars().all()]

    async def process(self) -> CartRes | dict:
        cart = await self.__cart_service.select_cart()
        if cart is None:
            self.__response.status_code = fastapi.status.HTTP_204_NO_CONTENT
            return {}
        cart_products = await self.__select_cart_product(cart)
        return CartRes(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            product_ids=[c.product_id for c in cart_products],
        )


@app.get("/api/cart")
async def gc(
        service: __Service = Depends(),
) -> CartRes | dict:
    return await service.process()
