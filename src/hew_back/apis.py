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
from hew_back import app
import hew_back.user_follow.creator_follow_api


@app.get("/health")
async def health():
    return {"ok": True}
