import uuid

from fastapi import Depends

from hew_back import app, deps, mdls
from hew_back.token.__token_body import PostTokenBody
from hew_back.token.__token_res import TokenRes, ImgTokenRes


@app.post("/api/token")
async def post_token(body: PostTokenBody) -> TokenRes:
    tokens = body.new_tokens()
    return TokenRes.from_tokens(tokens)


@app.get("/api/token/refresh")
async def token_refresh(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_refresh_token)
) -> TokenRes:
    return TokenRes.from_tokens(token.renew_tokens())


@app.get("/api/token/image")
async def image_token(
        _: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token)
) -> ImgTokenRes:
    return ImgTokenRes.from_img_tokens(
        mdls.ImgJwtTokenData.new(
            mdls.ImgTokenType.upload, uuid.uuid4()
        ).new_img_tokens()
    )
