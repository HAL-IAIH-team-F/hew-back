from dataclasses import dataclass

from hew_back import tbls
from hew_back.recommend.__res import GetRecommendRes


@dataclass
class RecommendResult:
    product: tbls.ProductTable

    def products_res(self) -> GetRecommendRes:
        return GetRecommendRes(
            product_id=self.product.product_id,
            product_thumbnail_uuid=self.product.product_thumbnail_uuid
        )
