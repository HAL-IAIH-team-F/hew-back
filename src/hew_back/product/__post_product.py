from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hew_back import deps, tbls, mdls
from hew_back.product import __result
from hew_back.product.__body import PostProductBody
from hew_back.tbls import CreatorProductTable


async def __insert_product(
        body: PostProductBody,
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> tbls.ProductTable:
    result = tbls.ProductTable.insert(
        session,
        product_price=body.price,
        product_title=body.product_title,
        product_description=body.product_description,
        listing_date=body.purchase_date,
        product_thumbnail_uuid=body.product_thumbnail_uuid,
        product_contents_uuid=body.product_contents_uuid,
    )
    await session.flush()
    await session.refresh(result)
    return result


async def __insert_creator_product(
        product: tbls.ProductTable = Depends(__insert_product),
        creator: deps.CreatorDeps = Depends(deps.CreatorDeps.get),
        session: AsyncSession = Depends(deps.DbDeps.session),
) -> CreatorProductTable:
    result = tbls.CreatorProductTable.insert(
        session, creator.creator_table, product
    )
    await session.flush()
    await session.refresh(result)
    return result


async def __post_images(
        body: PostProductBody,
        img_deps: deps.ImageDeps = Depends(deps.ImageDeps.get),
):
    img_deps.crete(mdls.State.public).post_preference(body.product_thumbnail_uuid)
    img_deps.crete(mdls.State.private).post_preference(body.product_contents_uuid)


async def post_product(
        product: tbls.ProductTable = Depends(__insert_product),
        creator_product: tbls.CreatorProductTable = Depends(__insert_creator_product),
        _img=Depends(__post_images),
) -> __result.PostCreatorResult:
    return __result.PostCreatorResult(
        product, creator_product
    )
