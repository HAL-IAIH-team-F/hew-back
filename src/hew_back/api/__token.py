from hew_back import app, model


@app.post("/api/token")
async def post_token(body: model.PostTokenBody):
    return model.TokenRes.create_by_post_token_body(body)
