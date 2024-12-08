import datetime
import uuid
from typing import Union, List, Sequence

import sqlalchemy

from sqlalchemy import select, or_, func, Column, String, DateTime, UUID, update
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import tbls
from hew_back.db import BaseTable
# from hew_back.tbls import
from hew_back.util import OrderDirection

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hew_back.tbls import ProductTag, CreatorProductTable, CreatorTable



class ProductTable(BaseTable):
    __tablename__ = 'TBL_PRODUCT'

    product_id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, default=uuid.uuid4)
    product_price = Column(sqlalchemy.Integer, nullable=False)
    product_title = Column(String(64), nullable=False)
    product_description = Column(String(255), nullable=False)
    purchase_date: datetime.datetime = Column(DateTime, default=datetime.datetime.now)
    product_thumbnail_uuid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    product_contents_uuid: uuid.UUID = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    @staticmethod
    def insert(
            session: AsyncSession,
            product_price: int,
            product_title: str,
            product_description: str,
            purchase_date: datetime.datetime,
            product_thumbnail_uuid: uuid.UUID,
            product_contents_uuid: uuid.UUID,
    ) -> 'ProductTable':
        table = ProductTable(
            product_price=product_price,
            product_title=product_title,
            product_description=product_description,
            purchase_date=purchase_date,
            product_thumbnail_uuid=product_thumbnail_uuid,
            product_contents_uuid=product_contents_uuid,
        )
        session.add(table)
        return table

    @staticmethod
    async def find_products_or_null(
            session: AsyncSession,
            name: Union[List[str], None],
            tag: Union[List[str], None],
            post_by: Union[List[str], None],
            start_datetime: Union[datetime, None],
            end_datetime: Union[datetime, None],
            following: Union[bool, None],
            read_limit_number: Union[int, None],
            time_order: OrderDirection,
            name_order: OrderDirection,
            like_order: OrderDirection,
            sort: List[str]
    ):
        stmt = select(ProductTable)

        if name is not None and len(name) > 0:
            stmt = stmt.where(
                or_(*[ProductTable.product_title.like(f"%{keyword}%") for keyword in name])
            )

        if tag is not None and len(tag) > 0:
            tag_subquery = (
                select(
                    tbls.ProductTag.item_id.label("product_id")
                )
                .join(tbls.Tag, tbls.ProductTag.tag_id == tbls.Tag.tag_id)
                .where(tbls.Tag.tag_name.in_(tag))
                # ProductTag.item_idをgroup_byすることで、ProductTag テーブルの item_id（製品ID）ごとにグループ化
                # →中間テーブルの特性上、その製品に関連付けられたタグ情報がまとめられる
                .group_by(tbls.ProductTag.item_id)
                # 各 item_id に関連するタグの数が指定した条件と一致したら
                .having(func.count(tbls.ProductTag.tag_id) == len(tag))
                .subquery()
            )
            # メインクエリにサブクエリを結合して、製品をフィルタリングしています
            stmt = stmt.join(tag_subquery, ProductTable.product_id == tag_subquery.c.product_id)

        if start_datetime is not None:
            start_datetime = start_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.purchase_date >= start_datetime)

        if end_datetime is not None:
            end_datetime = end_datetime.replace(tzinfo=None)
            stmt = stmt.where(ProductTable.purchase_date <= end_datetime)

        if post_by is not None and len(post_by) > 0:
            post_by_subquery = (
                select(
                    tbls.CreatorProductTable.product_id.label("product_id")
                )
                .join(tbls.CreatorTable, tbls.CreatorProductTable.creator_id == tbls.CreatorTable.creator_id)
                .join(tbls.UserTable, tbls.UserTable.user_id == tbls.CreatorTable.user_id)
                .where(tbls.UserTable.user_name.in_(post_by))
                .group_by(tbls.CreatorProductTable.product_id)
                .having(func.count(tbls.UserTable.user_name) == len(post_by))
                .subquery()
            )
            stmt = stmt.join(post_by_subquery, ProductTable.product_id == post_by_subquery.c.product_id)

        # ログイン機能を作らないときのAPIは役に立ちません　→　ログイン機能作ったら、where句追加してください
        if following:
            following_subquery = (
                select(
                    tbls.UserFollowTable.creator_id
                )
                # .where(UserFollowTable.user_id == current_user.user_id) ←　ログイン機能実装後、ログインしているユーザーがフォローしているクリエイターのフィルタリングを行う処理をwhere句で実施していきたい
                .subquery()
            )
            stmt = (
                select(ProductTable)
                .join(tbls.CreatorProductTable, ProductTable.product_id == tbls.CreatorProductTable.product_id)
                .join(tbls.CreatorTable, tbls.CreatorProductTable.creator_id == tbls.CreatorTable.creator_id)
                .where(tbls.CreatorProductTable.creator_id.in_(following_subquery))
            )

        if read_limit_number is not None and read_limit_number > 0:
            stmt = stmt.limit(read_limit_number)

        # time_order に基づいて product_date のソートを追加
        if time_order == OrderDirection.ASC:
            stmt = stmt.order_by(ProductTable.purchase_date.asc())
        elif time_order == OrderDirection.DESC:
            stmt = stmt.order_by(ProductTable.purchase_date.desc())
        #
        # name_order に基づいて product_title のソートを追加
        if name_order == OrderDirection.ASC:
            stmt = stmt.order_by(ProductTable.product_title.asc())
        elif name_order == OrderDirection.DESC:
            stmt = stmt.order_by(ProductTable.product_title.desc())

        likes_subquery = (
            select(
                tbls.LikeTable.product_id,
                func.count(tbls.LikeTable.product_id).label("like_count")
            )
            .group_by(tbls.LikeTable.product_id)
            .subquery()
        )
        stmt = stmt.outerjoin(likes_subquery, ProductTable.product_id == likes_subquery.c.product_id)

        if like_order == OrderDirection.ASC:
            stmt = stmt.order_by(likes_subquery.c.like_count.asc().nullsfirst())
        else:
            stmt = stmt.order_by(likes_subquery.c.like_count.desc().nullslast())

        if sort:
            print(sort)
            for sort_field in sort:
                print(sort_field)
                if sort_field == "datetime":
                    stmt = stmt.order_by(ProductTable.purchase_date.desc())  # datetime のデフォルトは降順
                elif sort_field == "name":
                    stmt = stmt.order_by(ProductTable.product_title.asc())  # name のデフォルトは昇順
                elif sort_field == "like":
                    stmt = stmt.order_by(likes_subquery.c.like_count.desc().nullslast())  # like のデフォルトは降順

        result = await session.execute(stmt)

        products = result.scalars().all()

        return products


    @staticmethod
    async def get_cart_products(
            session: AsyncSession,
            user_id: tbls.UserTable,
    ) -> Sequence["ProductTable"]:
        # 該当するユーザー
        stmt = (
            select(tbls.ProductTable)
            .join(tbls.CartProductTable, tbls.ProductTable.product_id == tbls.CartProductTable.product_id)
            .join(tbls.CartTable, tbls.CartProductTable.cart_id == tbls.CartTable.cart_id)
            .where(tbls.CartTable.user_id == user_id)
            .where(tbls.CartTable.purchase_date == None)
        )
        result = await session.execute(stmt)
        product_cart = result.scalars().all()
        return list(product_cart)

    @staticmethod
    async def cart_buy(
        session: AsyncSession,
        user_id: tbls.UserTable,
    ):
        subquery = (
            select(tbls.CartTable.cart_id)
            .where(tbls.CartTable.user_id == user_id)
            .where(tbls.CartTable.purchase_date == None)
        )

        stmt = (
            update(tbls.CartTable)
            .where(tbls.CartTable.cart_id.in_(subquery))
            .values(purchase_date=datetime.datetime.now(datetime.UTC).replace(tzinfo=None))
        )

        await session.execute(stmt)
        await session.commit()




    @staticmethod
    async def get_tags_for_product(
            session: AsyncSession,
            product_id: uuid,
    ) -> list[str]:
        """商品IDから関連タグを取得"""
        query = (
            select(tbls.Tag.tag_name)
            .join(ProductTag, tbls.Tag.tag_id == tbls.ProductTag.tag_id)
            .where(ProductTag.item_id == product_id)
        )
        result = await session.execute(query)
        return list(result.scalars())


    @staticmethod
    async def get_followed_creator_products_by_tags(
            session: AsyncSession,
            timeline_disp_user_id: tbls.UserTable.user_id,
            size: int,
            subquery_tags: list[str]
    ) -> Sequence["ProductTable"]:
        """フォロー中のクリエイター商品をタグに基づいて取得"""
        query = (
            select(ProductTable)
            .join(tbls.CreatorProductTable, ProductTable.product_id == tbls.CreatorProductTable.product_id)
            .join(tbls.UserFollowTable, tbls.CreatorProductTable.creator_id == tbls.UserFollowTable.creator_id)
            .where(tbls.UserFollowTable.user_id == timeline_disp_user_id)  # ログインしているユーザー、または指定ユーザーがフォローしているクリエイター
            .where(ProductTag.tag_id.in_(subquery_tags))
            .order_by(ProductTable.purchase_date.desc())
            .limit(size)
        )
        result = await session.execute(query)
        return result.scalars().all()


    @staticmethod
    async def get_product_creator(
            session: AsyncSession,
            product_id: uuid,
    ):
        """クエリパラメーターからのproduct_idからクリエイターIDを取得"""
        query = (
            select(tbls.CreatorTable.creator_id)
            .join(tbls.CreatorProductTable, CreatorTable.creator_id == tbls.CreatorProductTable.creator_id)
            .join(tbls.ProductTable, CreatorProductTable.product_id == product_id)
        )
        product_creator_id = await session.execute(query)
        return product_creator_id


    @staticmethod
    async def get_followed_creator_products_by_except_tags(
        session: AsyncSession,
        remaining_size: int,
        product_id: product_id,
        excluded_products: Sequence["ProductTable"],
    ) -> Sequence["ProductTable"]:
        """フォロー中のクリエイターの商品をタグ以外で取得"""
        excluded_products = [product.product_id for product in excluded_products]
        product_creator_id = ProductTable.get_product_creator(session, product_id)
        query = (
            select(ProductTable)
            .join(tbls.CreatorProductTable, ProductTable.product_id == tbls.CreatorProductTable.product_id)
            .join(tbls.UserFollowTable, tbls.CreatorProductTable.creator_id == tbls.UserFollowTable.creator_id)
            .where(CreatorProductTable.product_id.notin_(excluded_products)) # ←　多分、ここ違う気がする
            .where(product_creator_id == tbls.CreatorProductTable.creator_id)
            .order_by(ProductTable.purchase_date.desc())
            .limit(remaining_size)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_products_from_tags_except_order1_order2(
            session: AsyncSession,
            remaining_size: int,
            subquery_tags,
            excluded_products: Sequence["ProductTable"],
    ) -> Sequence["ProductTable"]:
        """商品タグからProductTableから最新順に取得"""
        product_tag = [product_tag for product_tag in subquery_tags]
        query = (
            select(ProductTable)
            .join(ProductTag, ProductTable.product_id == tbls.ProductTag.item_id)
            .where(ProductTag.tag_id.in_(product_tag))
            .where(CreatorProductTable.product_id.notin_(excluded_products))
            .order_by(ProductTable.purchase_date.desc())
            .limit(remaining_size)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_the_others_products(
            session: AsyncSession,
            remaining_size: int,
            excluded_products: Sequence["ProductTable"],
    ) -> Sequence["ProductTable"]:
        """ProductTableから最新準に取得"""
        query = (
            select(ProductTable)
            .where(CreatorProductTable.product_id.notin_(excluded_products))
            .order_by(ProductTable.purchase_date.desc())
            .limit(remaining_size)
        )
        result = await session.execute(query)
        return result.scalars().all()
