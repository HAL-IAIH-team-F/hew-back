from hew_back import app, model


@app.post("/api/token")
async def post_token(body: model.PostTokenBody):
    
    return {"ok": True}
