# noinspection PyUnresolvedReferences
import hew_back.chat.chat_api
# noinspection PyUnresolvedReferences
import hew_back.product.product_api
# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
import hew_back.token.token_api
# noinspection PyUnresolvedReferences
import hew_back.creator.creator_api
# noinspection PyUnresolvedReferences
import hew_back.user.user_api
# noinspection PyUnresolvedReferences
import hew_back.recruit.recruit_api
from hew_back import app
# noinspection PyUnresolvedReferences
import hew_back.follow.user_follow_api
# noinspection PyUnresolvedReferences
import hew_back.recruit.get_recruits
# noinspection PyUnresolvedReferences
import hew_back.token.get_token
# noinspection PyUnresolvedReferences
import hew_back.colab.post_colab_request
# noinspection PyUnresolvedReferences
import hew_back.notification.get_notifications
import hew_back.recommend.recommend_api


@app.get("/health")
async def health():
    return {"ok": True}
