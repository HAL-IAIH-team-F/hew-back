import uuid

import pydantic
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, tbls
from hew_back.cart.__reses import CartRes
from hew_back.cart.cart_service import CartService
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostCartBody:
    products: list[uuid.UUID]


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
    async def __validate_cart_is_none(cart: tbls.CartTable):
        if cart is None:
            return
        raise err.ErrorIds.INTERNAL_ERROR.to_exception(
            "A cart already exists for this user and has not been completed.")

    async def __insert_cart_products(self, cart: tbls.CartTable):
        cart_products = list[tbls.CartProductTable]()
        for product_id in self.__body.products:
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

    async def process(self):
        cart = await self.__cart_service.select_or_insert_cart()
        await self.__validate_cart_is_none(cart)
        cart = await self.__insert_cart()
        cart_products= await self.__insert_cart_products(cart)
        return CartRes(
            cart_id=cart.cart_id,
            user_id=cart.user_id,
            product_ids=[c.product_id for c in cart_products]
        )


@app.post("/api/cart")
async def pc(
        service: __Service = Depends(),
):
    return await service.process()

