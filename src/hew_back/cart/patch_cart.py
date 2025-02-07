import uuid
from dataclasses import field

import pydantic
import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import app, deps, tbls
from hew_back.cart.cart_service import CartService


@pydantic.dataclasses.dataclass
class PatchCartBodyRmProducts:
    rm_products: tuple[uuid.UUID] = field(default_factory=list)


@pydantic.dataclasses.dataclass
class PatchCartBodyRmAll:
    rm_all: bool = False


@pydantic.dataclasses.dataclass
class PatchCartBody:
    new_products: list[uuid.UUID] = field(default_factory=list)
    rm: PatchCartBodyRmProducts | PatchCartBodyRmAll = field(default_factory=PatchCartBodyRmAll)


@pydantic.dataclasses.dataclass
class CartPatchRes:
    new_products_filtered: list[uuid.UUID]
    rm_products_filtered: list[uuid.UUID]


class __Service:
    def __init__(
            self,
            body: PatchCartBody,
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

    async def __remove_cart_products(
            self, ids: list[uuid.UUID], cart: tbls.CartTable
    ) -> list[tbls.CartProductTable]:
        row = await self.__session.execute(
            sqlalchemy.select(tbls.CreatorProductTable)
            .where(
                tbls.CartProductTable.cart_id == cart.cart_id,
                tbls.CreatorProductTable.product_id.in_(ids),
                tbls.CartProductTable.removed == False
            )
        )
        result: list[tbls.CartProductTable] = [*row.scalars().all()]
        for product in result:
            product.removed = True
        await self.__session.flush()
        return result

    async def __remove_all_products(self, cart: tbls.CartTable):
        row = await self.__session.execute(
            sqlalchemy.select(
                sqlalchemy.select(tbls.CartProductTable).where(
                    tbls.CartProductTable.cart_id == cart.cart_id,
                    tbls.CartProductTable.removed == False
                )
            )
        )
        result: list[tbls.CartProductTable] = [*row.scalars().all()]
        for product in result:
            product.removed = True
        await self.__session.flush()

    async def process_rm(self, registered_cart_products: list[tbls.CartProductTable], cart: tbls.CartTable):
        if self.__body.rm is PatchCartBodyRmProducts:
            unregistered_rm_product_ids, registered_rm_product_ids = await self.__cart_service.sort_new_product_ids(
                registered_cart_products, self.__body.rm.rm_products
            )
            await self.__remove_cart_products(registered_rm_product_ids, cart)
            return unregistered_rm_product_ids
        elif self.__body.rm.rm_all:
            await self.__remove_all_products(cart)
            return []
        else:
            return []

    async def process(self):
        print(self.__body)
        cart = await self.__cart_service.select_or_insert_cart()
        registered_cart_products = await self.__cart_service.select_cart_product(cart)
        unregistered_rm_product_ids = await self.process_rm(registered_cart_products, cart)
        unregistered_new_product_ids, registered_new_product_ids = await self.__cart_service.sort_new_product_ids(
            registered_cart_products, self.__body.new_products
        )
        await self.__insert_cart_products(cart, unregistered_new_product_ids)
        return CartPatchRes(
            new_products_filtered=registered_new_product_ids,
            rm_products_filtered=unregistered_rm_product_ids,
        )


@app.patch("/api/cart")
async def pac(
        service: __Service = Depends(),
):
    return await service.process()
