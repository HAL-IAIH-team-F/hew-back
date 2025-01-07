import sqlalchemy
from fastapi import Depends

from hew_back import deps, tbls


class CartService:
    def __init__(
            self,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.__session = session
        self.__user = user

    async def select_cart(self) -> tbls.CartTable:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartTable)
            .where(sqlalchemy.and_(
                tbls.CartTable.user_id == self.__user.user_table.user_id,
                tbls.CartTable.purchase_date == None,
                ))
        )
        return raw.scalar_one_or_none()

