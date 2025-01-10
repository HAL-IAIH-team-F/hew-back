from typing import Union

from fastapi import Depends

from hew_back import app, deps
from hew_back.product.__res import *
from hew_back.util.err import ErrorIds


@app.put("/api/cart_buy")
async def cart_buy(
        session: AsyncSession = Depends(deps.DbDeps.session),
        user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
) -> None:
    user_id = user_deps.user_table.user_id
    remove_false_cart = await CartProduct.cart_buy(
        session=session,
        user_id=user_id,
    )
    if remove_false_cart:
        raise ErrorIds.INTERNAL_ERROR.to_exception("cart buy error")
    return
