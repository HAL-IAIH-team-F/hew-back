import uuid

import pydantic
import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps, tbls
from hew_back.cart.cart_service import CartService


@pydantic.dataclasses.dataclass
class PostCartBody:
    new_products = tuple[uuid.UUID]()
    rm_products = tuple[uuid.UUID]()


class __Service:
    def __init__(
            self,
            body: PostCartBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
            cart_service: CartService = Depends(),
    ):
        self.__session: AsyncSession = session
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

    async def __unregistered_new_product_ids(
            self, registered_cart_products: list[tbls.CartProductTable]
    ) -> list[uuid.UUID]:
        ids = list[uuid.UUID](self.__body.new_products)
        for prev in registered_cart_products:
            if prev.product_id in ids:
                ids.remove(prev.product_id)
        return ids

    async def __remove_cart_products(self) -> list[tbls.CartProductTable]:
        row = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorProductTable)
            .where(tbls.CreatorProductTable.product_id.in_(self.__body.rm_products))
        )
        result: list[tbls.CartProductTable] = [*row.scalars().all()]
        for product in result:
            product.removed = True
        await self.__session.flush()
        return result

    async def process(self):
        cart = await self.__cart_service.select_or_insert_cart()
        registered_cart_products = await self.__cart_service.select_cart_product(cart)
        new_product_ids = await self.__unregistered_new_product_ids(registered_cart_products)
        await self.__insert_cart_products(cart, new_product_ids)
        await self.__remove_cart_products()
        return


@app.patch("/api/cart")
async def pac(
        service: __Service = Depends(),
):
    return await service.process()
