import pydantic
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, tbls
from hew_back.util import err


@pydantic.dataclasses.dataclass
class PostCartBody:
    pass


class __Service:
    def __init__(
            self,
            body: PostCartBody,
            session: sqlalchemy.ext.asyncio.AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps = Depends(deps.UserDeps.get),
    ):
        self.__session = session
        self.__user = user
        self.__body = body

    async def __insert_cart(self):
        cart = tbls.CartTable(
            user_id=self.__user.user_table.user_id,
        )
        self.__session.add(cart)
        await self.__session.flush()
        await self.__session.refresh(cart)
        return cart

    @staticmethod
    async def __validate_cart_is_none(cart: tbls.CartTable):
        if cart is None:
            return
        raise err.ErrorIds.INTERNAL_ERROR.to_exception(
            "A cart already exists for this user and has not been completed.")

    async def __select_cart(self) -> tbls.CartTable:
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartTable)
            .where(sqlalchemy.and_(
                tbls.CartTable.user_id == self.__user.user_table.user_id,
                tbls.CartTable.purchase_date == None,
            ))
        )
        return raw.scalar_one_or_none()

    async def process(self):
        cart = await self.__select_cart()
        await self.__validate_cart_is_none(cart)
        await self.__insert_cart()


@app.post("/api/cart")
async def pc(
        service: __Service = Depends(),
) -> None:
    return await service.process()
