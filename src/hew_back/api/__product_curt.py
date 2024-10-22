from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from hew_back import app, deps, responses


@app.get("/product_cart/")
async def read_product_curt(
    session: AsyncSession = Depends(deps.DbDeps.session)
    ):
    product_cart = await responses.GetProductCart.get_product_cart(session=session)
    return product_cart