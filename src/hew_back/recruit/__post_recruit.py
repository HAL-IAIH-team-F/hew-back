import pydantic.dataclasses
from fastapi import Depends

from hew_back import tbls, deps
from hew_back.recruit.__reses import PostRecruitRes
from hew_back.tbls import RecruitTable


@pydantic.dataclasses.dataclass
class PostRecruitBody:
    title: str
    description: str


async def __insert_recruit(
        body: PostRecruitBody,
        session=Depends(deps.DbDeps.session),
        creator: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
) -> RecruitTable:
    result = tbls.RecruitTable.insert(
        session,
        creator.creator_table, body.title, body.description
    )
    await session.flush()
    await session.refresh(result)
    return result


async def post_recruit(
        recruit: RecruitTable = Depends(__insert_recruit),
) -> PostRecruitRes:
    return PostRecruitRes(
        recruit.recruit_id, recruit.creator_id, recruit.title, recruit.description
    )
