from fastapi import Depends

from hew_back import app
from hew_back.product import __post_product
from hew_back.product.__res import ProductRes


@app.post("/api/product")
async def pp(
        result=Depends(__post_product.post_product),
) -> ProductRes:
    return result.to_product_res()
