# noinspection PyUnresolvedReferences
import hew_back.chat.chat_api
# noinspection PyUnresolvedReferences
import hew_back.product.product_api
# noinspection PyUnresolvedReferences
import hew_back.token.token_api
# noinspection PyUnresolvedReferences
import hew_back.creator.creator_api
# noinspection PyUnresolvedReferences
import hew_back.user.user_api
import hew_back.product.cart_product_api
from hew_back import app


@app.get("/health")
async def health():
    return {"ok": True}
