from fastapi import Query

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from hew_back import app, deps, responses

import uuid

from typing import Union



@app.get("/product_cart")
async def read_product_curt(
    session: AsyncSession = Depends(deps.DbDeps.session),
    user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
    ):

    user_id = user_deps.user_table.user_id
    user_mail = user_deps.user_table.user_mail
    user_name = user_deps.user_table.user_name

    print("user_id:",user_id)
    print("user_mail:",user_mail)
    print("user_name:",user_name)

    if user_deps is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    product_cart = await responses.GetProductCart.get_product_cart(
        session=session,
        user_id=user_id,
        user_mail=user_mail,
        user_name=user_name,
    )

    if not product_cart:
        return {"detail": "商品カートに商品は追加されていません"}

    return product_cart

@app.put("/product_cart")
async def put_product_curt(
    session: AsyncSession = Depends(deps.DbDeps.session),
    product_id :Union[list[uuid.UUID], None] = Query(),
    user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
):
    user_id = user_deps.user_table.user_id
    remove_false_cart = await responses.PutProductCart.put_product_cart(
        session=session,
        product_id=product_id,
        user_id=user_id,
    )
    if remove_false_cart:
        return remove_false_cart
    return {}
