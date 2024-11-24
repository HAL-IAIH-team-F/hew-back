from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from hew_back import app, deps, product
from typing import Union
from hew_back.product.__res import *


@app.get("/api/product_cart")
async def read_product_cart(
     session: AsyncSession = Depends(deps.DbDeps.session),
     user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
     ):

     user_id = user_deps.user_table.user_id

     product_cart = await CartProduct.get_cart_product(
         session=session,
         user_id=user_id,
     )
     return product_cart


@app.put("/api/cart_buy")
async def cart_buy(
    session: AsyncSession = Depends(deps.DbDeps.session),
    user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
):
    user_id = user_deps.user_table.user_id
    remove_false_cart = await CartProduct.cart_buy(
        session=session,
        user_id=user_id,
    )
    if remove_false_cart:
        return remove_false_cart
    return {}

