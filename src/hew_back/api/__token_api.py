import uuid

from fastapi import Depends

from hew_back import app, bodies, reses, deps, mdls


@app.post("/api/token")
async def post_token(body: bodies.PostTokenBody) -> reses.TokenRes:
    tokens = body.new_tokens()
    return reses.TokenRes.from_tokens(tokens)


@app.get("/api/token/refresh")
async def token_refresh(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_refresh_token)
) -> reses.TokenRes:
    return reses.TokenRes.from_tokens(token.renew_tokens())


@app.get("/api/token/image")
async def image_token(
        _: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token)
) -> reses.ImgTokenRes:
    return reses.ImgTokenRes.from_img_tokens(
        mdls.ImgJwtTokenData.new(
            mdls.ImgTokenType.upload, uuid.uuid4()
        ).new_img_tokens()
    )
