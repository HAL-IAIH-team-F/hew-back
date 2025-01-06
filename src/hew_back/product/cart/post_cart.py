import pydantic
import sqlalchemy
from fastapi import Depends

from hew_back import app, deps, tbls


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

    async def process(self):
        await self.__insert_cart()


@app.post("/api/cart")
async def cart_buy(
        service: __Service = Depends(),
) -> None:
    return await service.process()
