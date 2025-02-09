import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls, mdls, app
from hew_back.product.__body import PostProductBody
from hew_back.product.__res import ProductRes
from hew_back.product.product_service import ProductService
from hew_back.tbls import CreatorProductTable


async def post_images(
        body: PostProductBody,
        img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
):
    img_deps.crete(mdls.State.public).post_preference(body.product_thumbnail_uuid)
    img_deps.crete(mdls.State.private).post_preference(body.product_contents_uuid)


class __Service:
    def __init__(
            self,
            body: PostProductBody,
            product_service: ProductService = Depends(),
            session: AsyncSession = Depends(deps.DbDeps.session),
            _img=Depends(post_images),
            creator: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
    ):
        self.__body = body
        self.__session = session
        self.__img = _img
        self.__creator = creator
        self.__product_service = product_service

    async def __insert_product(
            self,
    ) -> tbls.ProductTable:
        result = tbls.ProductTable(
            product_price=self.__body.price,
            product_title=self.__body.product_title,
            product_description=self.__body.product_description,
            purchase_date=self.__body.purchase_date,
            product_thumbnail_uuid=self.__body.product_thumbnail_uuid,
            product_contents_uuid=self.__body.product_contents_uuid,
        )
        self.__session.add(result)
        await self.__session.flush()
        await self.__session.refresh(result)
        return result

    async def __select_collaborators(self) -> list[tbls.CreatorTable]:
        result = list[tbls.CreatorTable]()
        for creator_id in self.__body.collaborator_ids:
            if creator_id == self.__creator.creator_table.creator_id:
                continue
            raw = await self.__session.execute(
                sqlalchemy.select(tbls.CreatorTable)
                .where(tbls.CreatorTable.creator_id == creator_id)
            )
            result.append(raw.scalar_one())
        return result

    async def __insert_creator_product(
            self,
            product: tbls.ProductTable,
            creators: list[tbls.CreatorTable]
    ) -> list[CreatorProductTable]:
        creator_products = list[CreatorProductTable]()
        for creator in creators:
            creator_product = CreatorProductTable(
                creator_id=creator.creator_id,
                product_id=product.product_id,
            )
            self.__session.add(creator_product)
            creator_products.append(creator_product)

        await self.__session.flush()
        for creator_product in creator_products:
            await self.__session.refresh(creator_product)
        return creator_products

    async def process(self):
        product = await self.__insert_product()
        collaborators = await self.__select_collaborators()
        creator_product = await self.__insert_creator_product(product, [*collaborators, self.__creator.creator_table])
        return ProductRes(
            product_id=product.product_id,
            product_price=product.product_price,
            product_title=product.product_title,
            product_description=product.product_description,
            purchase_date=product.purchase_date,
            product_thumbnail_uuid=product.product_thumbnail_uuid,
            creator_ids=[c.creator_id for c in creator_product],
            purchase_info=None,
        )


@app.post("/api/product")
async def pp(
        service: __Service = Depends(),
) -> ProductRes:
    return await service.process()
