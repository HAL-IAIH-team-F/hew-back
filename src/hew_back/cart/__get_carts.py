from fastapi import Depends

from hew_back import deps
from hew_back.product.__res import CartProduct
from hew_back.cart.__reses import CartRes


async def get_carts(
        session=Depends(deps.DbDeps.session),
        user_deps=Depends(deps.UserDeps.get),
) -> list[CartRes]:
    user_id = user_deps.user_table.user_id

    carts = await CartProduct.get_cart_product(
        session=session,
        user_id=user_id,
    )
    responses: list[CartRes] = []

    for cart in carts:
        responses.append(CartRes(
            product_id=cart.product_id,
            product_price=cart.product_price,
            product_title=cart.product_title,
            product_description=cart.product_description,
            purchase_date=cart.purchase_date,
            product_contents_uuid=cart.product_contents_uuid,
            product_thumbnail_uuid=cart.product_thumbnail_uuid,
        ))
    return responses
