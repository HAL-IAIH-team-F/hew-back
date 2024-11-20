from dataclasses import dataclass

from hew_back import tbls
from hew_back.product.__res import ProductRes


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
