from fastapi import FastAPI
from pydantic import BaseModel

# データモデルを定義します
class PostCreatorModel(BaseModel):
    user: int
    contact_address: str
    transfer_target: float

# FastAPIアプリケーションを作成します
app = FastAPI()

# POSTリクエストを受け取るエンドポイントを定義します
@app.post("/PostCreatorModel/")
async def create_item(item: PostCreatorModel):
    # 受け取ったデータをそのまま返します
    return item
