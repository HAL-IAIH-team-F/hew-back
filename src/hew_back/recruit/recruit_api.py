from fastapi import Depends

from hew_back import app
from hew_back.product.__res import ProductRes
from hew_back.recruit.__post_recruit import post_recruit


@app.post("/api/recruit")
async def pr(
        result=Depends(post_recruit),
) -> ProductRes:
    return result.to_product_res()
