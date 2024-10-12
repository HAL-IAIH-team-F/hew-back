import uuid

from fastapi import Depends

from hew_back import app, bodies, responses, deps, models


@app.post("/api/token")
async def post_token(body: bodies.PostTokenBody) -> responses.TokenRes:
    tokens = body.new_tokens()
    return tokens.to_token_res()


@app.get("/api/token/refresh")
async def token_refresh(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_refresh_token)
) -> responses.TokenRes:
    return token.renew_tokens().to_token_res()


@app.get("/api/token/image")
async def image_token(
        _: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token)
) -> responses.ImgTokenRes:
    return models.ImgJwtTokenData.new(
        models.ImgTokenType.upload, uuid.uuid4()
    ).new_img_tokens().to_img_token_res()
