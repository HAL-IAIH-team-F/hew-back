from dataclasses import dataclass

from hew_back import tbls
from hew_back.product.__res import ProductRes, GetProductsResponse


@dataclass
class ProductsResult:
    products: list[tbls.ProductTable]

    def to_get_products_res(self):
        return [GetProductsResponse.create(
            product_description=product.product_description,
            product_id=product.product_id,
            product_thumbnail_uuid=product.product_thumbnail_uuid,
            product_price=product.product_price,
            product_title=product.product_title,
            listing_date=product.listing_date,
            product_contents_uuid=product.product_contents_uuid,
        ) for product in self.products]


@dataclass
class PostCreatorResult:
    product: tbls.ProductTable
    creator_product: tbls.CreatorProductTable

    def to_product_res(self) -> ProductRes:
        return ProductRes.create(
            product_id=self.product.product_id,
            product_price=self.product.product_price,
            product_title=self.product.product_title,
            product_description=self.product.product_description,
            listing_date=self.product.listing_date,
            product_thumbnail_uuid=self.product.product_thumbnail_uuid,
            product_contents_uuid=self.product.product_contents_uuid,
            creator_id=self.creator_product.creator_id,
        )
