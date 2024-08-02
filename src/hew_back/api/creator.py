from fastapi import FastAPI

from hew_back import app
from hew_back.request_model import PostCreatorBody

# FastAPIアプリケーションを作成します


# POSTリクエストを受け取るエンドポイントを定義します
@app.post("/creator")
async def post_creator(creator_box: PostCreatorBody):
    # 受け取ったデータをそのまま返します
    return creator_box.user_id
