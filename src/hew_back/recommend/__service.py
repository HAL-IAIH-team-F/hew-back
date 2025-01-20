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


    async def _fetch_protabs_by_pro_id_tag_id(self) -> list[RecommendResult]:
        """
        フォロー中のクリエイターとタグを考慮して製品テーブルを取得
        """
        tag_id_list: TagListResult = await self._get_tags_by_product_id()
        products = await self._fetch_products_with_priority(tag_id_list, self.target_id)
        return [RecommendResult(products=products)]

    # 共通処理
    async def _get_tags_by_product_id(self) -> TagListResult:
        """
            product_idからタグを取得
        """
        tags_ids = await self.session.execute(
            select(tbls.Tag.tag_id)
            .join(tbls.ProductTag, tbls.Tag.tag_id == ProductTag.tag_id)
            .join(tbls.ProductTable, tbls.ProductTable.product_id == ProductTable.product_id)
            .where(tbls.ProductTable.product_id == self.product_id)
        )
        return TagListResult(tags=list(tags_ids.scalars().all()))


    async def _fetch_products_with_priority(self, tag_ids: TagListResult, target_id: uuid.UUID) -> list[tbls.ProductTable]:
        """
            タイムライン対象のuser_idとタグに基づき製品を取得
        """
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
