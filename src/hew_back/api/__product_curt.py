from fastapi import Query

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from hew_back import app, deps, responses

import uuid

from typing import Union

@app.get("/product_cart")
async def read_product_curt(
    session: AsyncSession = Depends(deps.DbDeps.session)
    ):
    product_cart = await responses.GetProductCart.get_product_cart(session=session)
    return product_cart

@app.put("/product_cart")
async def put_product_curt(
    session: AsyncSession = Depends(deps.DbDeps.session),
    product_id :Union[list[uuid.UUID], None] = Query(),
):
    remove_prod_cart = await responses.PutProductCart.put_product_cart(
        session=session,
        product_id=product_id,
    )
    if product_id:
        # 処理
        return {"message": f"Product {product_id} updated"}
    return {"error": "No product_id provided"}
