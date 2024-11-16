from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from hew_back import app, deps, responses
from typing import Union


@app.get("/cart_product")
async def read_product_curt(
     session: AsyncSession = Depends(deps.DbDeps.session),
     user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
     ):

     user_id = user_deps.user_table.user_id

     if user_deps is None:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

     product_cart = await responses.CartProduct.get_cart_product(
         session=session,
         user_id=user_id,
     )
     return product_cart

@app.put("/cart_product")
async def put_cart_product(
    session: AsyncSession = Depends(deps.DbDeps.session),
     user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
):
    user_id = user_deps.user_table.user_id
    remove_false_cart = await responses.CartProduct.put_cart_product(
        session=session,
        user_id=user_id,
    )
    if remove_false_cart:
        return remove_false_cart
    return {}


#
# @app.put("/product_cart")
# async def put_product_curt(
#     session: AsyncSession = Depends(deps.DbDeps.session),
#     product_id :Union[list[uuid.UUID], None] = Query(),
#     user_deps: Union[deps.UserDeps, None] = Depends(deps.UserDeps.get),
# ):
#     user_id = user_deps.user_table.user_id
#     remove_false_cart = await responses.PutProductCart.put_product_cart(
#         session=session,
#         product_id=product_id,
#         user_id=user_id,
#     )
#     if remove_false_cart:
#         return remove_false_cart
#     return {}
#