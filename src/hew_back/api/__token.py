from fastapi import Depends

from hew_back import app, model


@app.post("/api/token")
async def post_token(body: model.PostTokenBody) -> model.TokenRes:
    return model.TokenRes.create_by_post_token_body(body)


@app.get("/api/token/refresh")
async def token_refresh(token: model.JwtTokenData = Depends(model.JwtTokenData.get_access_token_or_none)):
    return model.TokenRes.create_by_jwt_token_data(token)
