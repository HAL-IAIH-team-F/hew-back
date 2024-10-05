from fastapi import Depends

from hew_back import app, result, bodies, responses, deps


@app.post("/api/token")
async def post_token(body: bodies.PostTokenBody) -> responses.TokenRes:
    profile = body.fetch_keycloak_profile()
    return responses.TokenRes.create_by_keycloak_user_profile(profile)


@app.get("/api/token/refresh")
async def token_refresh(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_access_token_or_none)
) -> responses.TokenRes:
    return token.to_token_res()
