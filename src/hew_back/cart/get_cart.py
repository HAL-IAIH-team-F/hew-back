import fastapi
from fastapi import Depends

from hew_back import deps, app
from hew_back.cart.__reses import CartRes
from hew_back.product.__res import CartProduct


@app.get("/api/cart")
async def gc(
        response: fastapi.Response,
        session=Depends(deps.DbDeps.session),
        user_deps=Depends(deps.UserDeps.get),
) -> CartRes | dict:
    user_id = user_deps.user_table.user_id

    cart = await CartProduct.get_cart_product(
        session=session,
        user_id=user_id,
    )
    if cart is None:
        response.status_code = fastapi.status.HTTP_204_NO_CONTENT
        return {}
    return CartRes(
        product_id=cart.product_id,
        product_price=cart.product_price,
        product_title=cart.product_title,
        product_description=cart.product_description,
        purchase_date=cart.purchase_date,
        product_contents_uuid=cart.product_contents_uuid,
        product_thumbnail_uuid=cart.product_thumbnail_uuid,
    )
