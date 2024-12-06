from fastapi import Depends

from hew_back import deps, app
from hew_back.token.__reses import TokenRes


@app.get("/api/token")
async def gtr(
        token: deps.JwtTokenDeps = Depends(deps.JwtTokenDeps.get_refresh_token)
) -> TokenRes:
    return TokenRes.from_tokens(token.renew_tokens())
