from fastapi import Depends

from hew_back import app
from hew_back.recruit.__post_recruit import post_recruit
from hew_back.recruit.__reses import PostRecruitRes


@app.post("/api/recruit")
async def pr(
        response: PostRecruitRes = Depends(post_recruit),
) -> PostRecruitRes:
    return response
