from fastapi import Depends

from hew_back import app, tables, bodies


# FastAPIアプリケーションを作成します


# POSTリクエストを受け取るエンドポイントを定義します
@app.post("/creator")
async def post_creator(
        body: bodies.PostCreatorBody,
        user_tbl: tables.UserTable = Depends(tables.CreatorTable)
):
    body
    return body.user_id
