from dataclasses import dataclass

from hew_back import tbls
from hew_back.product.__res import ProductRes


@dataclass
class ProductsResult:
    products: list[tbls.ProductTable]

    def to_get_products_res(self):
        return [ProductRes(
            product_description=product.product_description,
            product_id=product.product_id,
            product_thumbnail_uuid=product.product_thumbnail_uuid,
            product_price=product.product_price,
            product_title=product.product_title,
            purchase_date=product.purchase_date,
            product_contents_uuid=product.product_contents_uuid,
        ) for product in self.products]
