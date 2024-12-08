import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls, deps

from hew_back.recommend.__result import RecommendResult
from hew_back.tbls import ProductTable


class RecommendGet:
    @staticmethod
    async def get_recommend(
            session: AsyncSession,
            user: deps.UserDeps,
            size: int,
            product_id: uuid.UUID,
            search_user_id: uuid.UUID,
    ) -> RecommendResult:

        # ログインしていない
        if user is None:
            pass
        # ログインしている
        else:
            user_id = user.user_table.user_id
            user_id_to_use = RecommendGet.get_decide_user_timeline(user_id, search_user_id)

            if product_id is None:
                pass
            else:
                return await RecommendGet.get_product_table_from_user_id_product_id(session, user_id_to_use, product_id, size)


    @staticmethod
    async def get_product_table_from_user_id_product_id(session, user_id_to_use, product_id, size):

        subquery_tags: list[str] = await ProductTable.get_tags_for_product(session, product_id)

        order1_products = await ProductTable.get_followed_creator_products_by_tags(
            session, user_id_to_use, size, subquery_tags
        )
        remaining_size = RecommendGet.get_remaining_size(size, len(order1_products))
        if remaining_size == 0:
            for product in order1_products:
                return RecommendResult(product)

        order2_products = await ProductTable.get_followed_creator_products_by_except_tags(
            session, size, product_id, order1_products
        )
        remaining_size = RecommendGet.get_remaining_size(size, len(order2_products))
        if remaining_size == 0:
            for product in order2_products:
                return RecommendResult(product)

        order3_products = await tbls.ProductTable.get_products_from_tags_except_order1_order2(
            session, size, subquery_tags, order2_products
        )
        remaining_size = RecommendGet.get_remaining_size(size, len(order3_products))
        if remaining_size == 0:
            for product in order3_products:
                return RecommendResult(product)

        order4_products = await tbls.ProductTable.get_the_others_products(
            session, size, order3_products
        )
        for product in order4_products:
            return RecommendResult(product)

    @staticmethod
    async def get_decide_user_timeline(
            user_id: tbls.UserTable.user_id,
            search_user_id: Optional[tbls.UserTable.user_id],
    ):
        if search_user_id:
            user_id_to_use = search_user_id
        else:
            user_id_to_use = user_id
        return user_id_to_use

    @staticmethod
    async def get_remaining_size(remaining_size: int, get_product_size: int) -> int:
        remaining_size = remaining_size - get_product_size
        return remaining_size