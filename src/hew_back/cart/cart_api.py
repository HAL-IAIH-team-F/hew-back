from typing import Union

from fastapi import Depends

from hew_back import app, deps
from hew_back.product.__res import *


@app.put("/api/cart_buy")
async def cart_buy(
        session: AsyncSession = Depends(deps.DbDeps.session),
        user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
) -> None:
    user_id = user_deps.user_table.user_id
    await CartProduct.cart_buy(
        session=session,
        user_id=user_id,
    )
