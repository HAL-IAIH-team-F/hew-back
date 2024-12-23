import uuid
from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import AsyncSession
from hew_back import tbls, deps
from hew_back.recommend.__result import RecommendResult
from hew_back.tbls import ProductTable, ProductTag, UserTable, CreatorProductTable, CreatorTable
from fastapi import Depends, Query
from typing_extensions import Optional
import sqlalchemy
from sqlalchemy import select
from hew_back.recommend.__res import GetRecommendRes


@dataclass
class TagListResult:
    tags: list[uuid.UUID] = field(default_factory=list)
    
@dataclass
class FollowedCreatorResult:
    creator_ids: list[uuid.UUID] = field(default_factory=list)


class __Service:
    def __init__(
            self,
            session: AsyncSession = Depends(deps.DbDeps.session),
            user_deps: deps.UserDeps = Depends(deps.UserDeps.get_or_none),
            size = Query(21, ge=21, le=30),
            product_id: Optional[uuid.UUID] = Query(default=None, description=""),
            search_user_id = Query(default=None, description=""),
        ):
        self.session = session
        self.size = size
        self.product_id = product_id
        self.target_id = search_user_id if search_user_id else user_deps.user_table.user_id

    async def request(self) -> list[RecommendResult]:
        if self.product_id and self.target_id:
            return await self._fetch_protabs_by_pro_id_tag_id()
        elif self.target_id:
            return await self._fetch_protab_by_tar_id()
        elif self.product_id:
            return await self._fetch_products_by_tag_only()
        else:
            return await self._fetch_latest_products_only()

    async def _fetch_protabs_by_pro_id_tag_id(self) -> list[RecommendResult]:
        """
        フォロー中のクリエイターとタグを考慮して製品テーブルを取得
        """
        tag_id_list: TagListResult = await self._get_tags_by_product_id()
        products = await self._fetch_products_with_priority(tag_id_list, self.target_id)
        return [RecommendResult(products=products)]

    async def _fetch_protabs_by_tar_id(self) -> list[RecommendResult]:
        """
        フォロー中のクリエイターから製品を取得
        """
        followed_creators = await self._get_followed_creators()
        products = await self._fetch_products_case_2(followed_creators)
        return RecommendResult(products).to_get_products_res()

    async def _fetch_protabs_by_tag(self) -> list[RecommendResult]:
        """
        product_idからタグを取得
        """
        pass

    # 共通処理
    async def _get_tags_by_product_id(self) -> TagListResult:
        """product_idからタグを取得"""
        tags_ids = await self.session.execute(
            select(tbls.Tag.tag_id)
            .join(tbls.ProductTag, tbls.Tag.tag_id == ProductTag.tag_id)
            .join(tbls.ProductTable, tbls.ProductTable.product_id == ProductTable.product_id)
            .where(tbls.ProductTable.product_id == self.product_id)
        )
        return TagListResult(tags=list(tags_ids.scalars().all()))

    async def _fetch_products_with_priority(self, tag_ids: TagListResult, target_id: uuid.UUID) -> list[tbls.ProductTable]:
        """タイムライン対象のuser_idとタグに基づき製品を取得"""
        stmt = (
            select(tbls.ProductTable)
            .join(tbls.ProductTag, ProductTable.product_id == ProductTag.item_id)
            .join(tbls.Tag, ProductTag.tag_id == tbls.Tag.tag_id)
            .join(tbls.CreatorProductTable, ProductTable.product_id == CreatorProductTable.product_id)
            .join(tbls.CreatorTable, CreatorProductTable.creator_id == CreatorTable.creator_id)
            .join(tbls.UserTable, CreatorTable.user_id == UserTable.user_id)
            .join(tbls.UserFollowTable, UserTable.user_id == tbls.UserFollowTable.user_id)
            .where(tbls.UserFollowTable.user_id == target_id)
            .where(ProductTag.tag_id.in_(tag_ids.tags)) # tag_idsがTagListResult型のオブジェクト→tag_idsからリストを抽出して使用する必要あり
            .limit(self.size)
        )
        protabls = await self.session.execute(stmt)
        return list(protabls.scalars().all()) # ← 型がSequence、SQLAlqumeyのSequenceはlist型とのことだが、明示的にした。

# 商品購入されているものとされていないものを再表示
# 存在しないproduct_idがあれば、その例外処理を実装する




# class RecommendGet:
#     @staticmethod
#     async def get_recommend(
#             session: AsyncSession,
#             user_deps: deps.UserDeps,
#             size: int,
#             product_id: uuid.UUID,
#             search_user_id: uuid.UUID,
#     ) -> RecommendResult:
#
#         # ログインしていない
#         if user_deps is None:
#             return await RecommendGet._handle_guest_user()
#         # ログインしている
#         return await RecommendGet._hangle_logged_user(
#             session, user_deps, size, product_id, search_user_id
#         )
#
#     @staticmethod
#     async def _handle_guest_user() -> None:
#         """ログインしていないユーザーの処理"""
#         return None
#
#     @staticmethod
#     async def _hangle_logged_user(
#         session: AsyncSession,
#         user_deps: deps.UserDeps,
#         size: int,
#         product_id: uuid.UUID,
#         search_user_id: uuid.UUID,
#     ) -> RecommendResult:
#         """ログインしているユーザーの処理"""
#         user_id = user_deps.user_table.user_id
#         # タイムライン画面がログインユーザーか他のユーザーのどちらかを決める
#         target_user_id = await RecommendGet.get_decide_user_timeline(user_id, search_user_id)
#
#         # product_idの有無の処理
#         if product_id is None:
#             return await RecommendGet.get_product_table_from_target_id()
#         return await RecommendGet.get_product_table_from_target_user_id_product_id(session, target_user_id, size, product_id)
#
#     @staticmethod
#     async def get_decide_user_timeline(
#             user_id: uuid.UUID,
#             search_user_id: uuid.UUID,
#     ) -> uuid.UUID:
#         """user_id（ログイン）かsearch_user_id(他のuser)を決定する処理"""
#         return search_user_id if search_user_id else user_id




    # @staticmethod
    # async def get_product_table_from_user_id_product_id(session, user_id_to_use, product_id, size):
    #
    #     subquery_tags: list[str] = await ProductTable.get_tags_for_product(session, product_id)
    #
    #     order1_products = await ProductTable.get_followed_creator_products_by_tags(
    #         session, user_id_to_use, size, subquery_tags
    #     )
    #     remaining_size = RecommendGet.get_remaining_size(size, len(order1_products))
    #     if remaining_size == 0:
    #         for product in order1_products:
    #             return RecommendResult(product)
    #
    #     order2_products = await ProductTable.get_followed_creator_products_by_except_tags(
    #         session, user_id_to_use, size, subquery_tags
    #     )
    #     remaining_size = RecommendGet.get_remaining_size(size, len(order2_products))
    #     if remaining_size == 0:
    #         for product in order2_products:
    #             return RecommendResult(product)
    #
    #     # ↓　引数が複雑なので、変更する必要あり
    #     order3_products = await tbls.ProductTable.get_products_from_tags_except_order1_order2(
    #         session, size, subquery_tags, order2_products
    #     )
    #     remaining_size = RecommendGet.get_remaining_size(size, len(order3_products))
    #     if remaining_size == 0:
    #         for product in order3_products:
    #             return RecommendResult(product)
    #
    #     order4_products = await tbls.ProductTable.get_the_others_products(
    #         session, size, order3_products
    #     )
    #     for product in order4_products:
    #         return RecommendResult(product)
    #
    # @staticmethod
    # async def get_decide_user_timeline(
    #         user_id: tbls.UserTable.user_id,
    #         search_user_id: Optional[tbls.UserTable.user_id],
    # ):
    #     if search_user_id:
    #         user_id_to_use = search_user_id
    #     else:
    #         user_id_to_use = user_id
    #     return user_id_to_use
    #
    # @staticmethod
    # async def get_remaining_size(remaining_size: int, get_product_size: int) -> int:
    #     remaining_size = remaining_size - get_product_size
    #     return remaining_size