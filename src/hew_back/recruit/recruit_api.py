from fastapi import Depends

from hew_back import app
from hew_back.recruit.__post_recruit import post_recruit
from hew_back.recruit.__reses import RecruitRes


@app.post("/api/recruit")
async def pr(
        response: RecruitRes = Depends(post_recruit),
) -> RecruitRes:
    return response
