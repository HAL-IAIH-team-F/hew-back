from typing import Union

from fastapi import Depends

from hew_back import app, deps
from hew_back.product.__res import *
from hew_back.product.cart.__get_carts import get_carts
from hew_back.product.cart.__reses import CartRes


@app.get("/api/product_cart")
async def read_product_cart(
        carts: list[CartRes] = Depends(get_carts),
) -> list[CartRes]:
    return carts


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
