from datetime import UTC

import sqlalchemy
from fastapi import Depends

from hew_back import app, deps
from hew_back.cart.__reses import CartRes
from hew_back.cart.cart_service import CartService
from hew_back.product.__res import *


class __Service:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            cart_service: CartService = Depends(),
    ):
        self.__session = session
        self.__user = user
        self.__cart_service = cart_service

    async def process(self):
        cart = await self.__cart_service.select_or_insert_cart()
        cart.purchase_date = datetime.now(UTC).replace(tzinfo=None)
        await self.__session.flush()
        cart_products = await self.__cart_service.select_cart_product(cart)
        return CartRes(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            product_ids=[c.product_id for c in cart_products],
        )


@app.put("/api/cart_buy")
async def cart_buy(
        service: __Service = Depends(),
) -> CartRes:
    return await service.process()
