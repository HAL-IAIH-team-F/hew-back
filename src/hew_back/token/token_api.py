import uuid

from fastapi import Depends

from hew_back import app, deps, mdls
from hew_back.token.__reses import TokenResOld, ImgTokenRes
from hew_back.token.__token_body import PostTokenBody


@app.post("/api/token")
async def post_token(body: PostTokenBody) -> TokenResOld:
    tokens = body.new_tokens()
    return TokenResOld.from_tokens(tokens)


@app.get("/api/token/refresh")
async def token_refresh(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_refresh_token)
) -> TokenResOld:
    return TokenResOld.from_tokens(token.renew_tokens())


@app.get("/api/token/file/upload")
async def gettfu(
        _: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token)
) -> ImgTokenRes:
    return ImgTokenRes.from_img_tokens(
        mdls.ImgJwtTokenData.new(
            mdls.ImgTokenType.upload, uuid.uuid4()
        ).new_img_tokens()
    )
