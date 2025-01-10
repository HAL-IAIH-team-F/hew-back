import uuid

import pydantic
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, tbls
from hew_back.cart.cart_service import CartService
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostCartBody:
    new_products: list[uuid.UUID]


class __Service:
    def __init__(
            self,
            body: PostCartBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            cart_service: CartService = Depends(),
    ):
        self.__session = session
        self.__user = user
        self.__body = body
        self.__cart_service = cart_service

    async def __insert_cart(self) -> tbls.CartTable:
        cart = tbls.CartTable(
            user_id=self.__user.user_table.user_id,
        )
        self.__session.add(cart)
        await self.__session.flush()
        await self.__session.refresh(cart)
        return cart

    @staticmethod
    async def __validate_cart_is_not_none(cart: tbls.CartTable):
        if cart is not None:
            return
        raise err.ErrorIds.INTERNAL_ERROR.to_exception("A cart not exists for this user and has not been completed.")

    async def __insert_cart_products(self, cart: tbls.CartTable, new_product_ids: list[uuid.UUID]):
        cart_products = list[tbls.CartProductTable]()
        for product_id in new_product_ids:
            cart_product = tbls.CartProductTable(
                cart_id=cart.cart_id,
                product_id=product_id,
            )
            cart_products.append(cart_product)
            self.__session.add_all(cart_products)
        await self.__session.flush()
        for cart_product in cart_products:
            await self.__session.refresh(cart_product)
        return cart_products

    async def __filter_registered_products(
            self, prev_cart_products: list[tbls.CartProductTable]
    ) -> list[uuid.UUID]:
        ids = list[uuid.UUID](self.__body.new_products)
        for prev in prev_cart_products:
            if prev.product_id in ids:
                ids.remove(prev.product_id)
        return ids

    async def process(self):
        cart = await self.__cart_service.select_cart()
        await self.__validate_cart_is_not_none(cart)
        prev_cart_products = await self.__cart_service.select_cart_product(cart)
        new_product_ids = await self.__filter_registered_products(prev_cart_products)
        await self.__insert_cart_products(cart, new_product_ids)
        return


@app.patch("/api/cart")
async def pac(
        service: __Service = Depends(),
):
    return await service.process()
