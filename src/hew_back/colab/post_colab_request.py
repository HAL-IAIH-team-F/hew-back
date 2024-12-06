from typing import Union, Sequence

import sqlalchemy.ext.asyncio
from fastapi import Depends, Query
from sqlalchemy import ColumnElement

from hew_back import deps, app
from hew_back.recruit.__reses import RecruitRes
from hew_back.tbls import RecruitTable


def search_stmt(
        name: Union[list[str], None] = Query(default=None),
) -> ColumnElement[bool]:
    if name is None or len(name) == 0:
        return sqlalchemy.true()
    return sqlalchemy.and_(
        *[sqlalchemy.or_(
            RecruitTable.title.like(f"%{keyword}%"),
            RecruitTable.description.like(f"%{keyword}%"),
        ) for keyword in name]
    )


async def find_recruits(
        session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
        search: ColumnElement[bool] = Depends(search_stmt),
        limit: Union[int, None] = Query(default=20),
) -> Sequence[RecruitTable]:
    result = await session.execute(
        sqlalchemy.select(RecruitTable)
        .where(search)
        .limit(limit)
    )
    result = result.scalars().all()
    await session.flush()
    for recruit in result:
        await session.refresh(recruit)
    return result


@app.post("/api/colab/request")
async def pcr(
        recruits: Sequence[RecruitTable] = Depends(find_recruits),
) -> list[RecruitRes]:
    result: list[RecruitRes] = []

    for recruit in recruits:
        result.append(RecruitRes(
            recruit.recruit_id, recruit.creator_id, recruit.title, recruit.description
        ))

    return result
