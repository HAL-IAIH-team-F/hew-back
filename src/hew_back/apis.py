# noinspection PyUnresolvedReferences
import hew_back.chat.chat_api
# noinspection PyUnresolvedReferences
import hew_back.chat.post_chat
# noinspection PyUnresolvedReferences
import hew_back.colab.post_colab_request
# noinspection PyUnresolvedReferences
import hew_back.colab.post_colab
# noinspection PyUnresolvedReferences
import hew_back.colab.post_colab_approve
# noinspection PyUnresolvedReferences
import hew_back.colab.post_colab_want
# noinspection PyUnresolvedReferences
import hew_back.creator.creator_api
# noinspection PyUnresolvedReferences
import hew_back.creator.get_creators
# noinspection PyUnresolvedReferences
import hew_back.creator.get_creator
# noinspection PyUnresolvedReferences
import hew_back.follow.user_follow_api
# noinspection PyUnresolvedReferences
import hew_back.notification.get_notifications
# noinspection PyUnresolvedReferences
import hew_back.cart.cart_api
# noinspection PyUnresolvedReferences
import hew_back.cart.get_cart
# noinspection PyUnresolvedReferences
import hew_back.cart.patch_cart
# noinspection PyUnresolvedReferences
import hew_back.cart.post_cart
# noinspection PyUnresolvedReferences
import hew_back.product.post_product
# noinspection PyUnresolvedReferences
import hew_back.product.get_products
# noinspection PyUnresolvedReferences
import hew_back.product.get_product
# noinspection PyUnresolvedReferences
import hew_back.recruit.get_recruits
# noinspection PyUnresolvedReferences
import hew_back.recruit.recruit_api
# noinspection PyUnresolvedReferences
import hew_back.token.get_token
# noinspection PyUnresolvedReferences
import hew_back.token.token_api
# noinspection PyUnresolvedReferences
import hew_back.user.user_api
# noinspection PyUnresolvedReferences
import hew_back.user.put_user
# noinspection PyUnresolvedReferences
import hew_back.user.get_user
# noinspection PyUnresolvedReferences
import hew_back.timeline.get_timeline
from hew_back import app


@app.get("/health")
async def health() -> dict:
    return {"ok": True}
