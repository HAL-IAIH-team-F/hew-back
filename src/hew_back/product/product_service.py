import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls, mdls
from hew_back.product.__res import PurchaseInfo


class ProductService:
    def __init__(
            self,
            session: AsyncSession = Depends(deps.DbDeps.session),
            user: deps.UserDeps | None = Depends(deps.UserDeps.get_or_none),
    ):
        self.__session = session
        self.__user = user

    async def select_cart(self, product: tbls.ProductTable) -> list[tbls.CartTable]:
        if self.__user is None:
            return []
        raw = await self.__session.execute(
            sqlalchemy.select(tbls.CartTable)
            .join(tbls.CartProductTable, tbls.CartTable.cart_id == tbls.CartProductTable.cart_id)
            .where(sqlalchemy.and_(
                tbls.CartProductTable.product_id == product.product_id,
                tbls.CartTable.purchase_date != None,
                tbls.CartTable.user_id == self.__user.user_table.user_id,
            ))
        )
        return [*raw.scalars().all()]

    @staticmethod
    def new_purchase_info(carts: list[tbls.CartTable] | None, product: tbls.ProductTable):
        if len(carts) == 0:
            return None

        token = mdls.FileAccessJwtTokenData.new(
            mdls.ImgTokenType.access, product.product_contents_uuid
        ).new_img_tokens()

        return PurchaseInfo(
            content_uuid=product.product_contents_uuid,
            token=token,
        )
