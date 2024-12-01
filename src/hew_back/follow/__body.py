import uuid

from pydantic.dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls
from pydantic import BaseModel

# result が標準のdataclass, データベースに登録
# __body がpydanticのdateclass,　__bodyで複数テーブルをreturn?sqlalquey型のやつをreturn

@dataclass
class UserFollow(BaseModel):
    creator_id: uuid.UUID

    async def save_new(self, user: deps.UserDeps, session: AsyncSession):
        user_id = user.user_table.user_id
        follow_id = uuid.uuid4()
        new_follow = tbls.UserFollowTable(
            follow_id=follow_id,
            user_id=user_id,
            creator_id=self.creator_id
        )
        session.add(new_follow)
        await session.commit()
