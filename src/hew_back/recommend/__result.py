from dataclasses import dataclass
from hew_back import tbls
from hew_back.recommend.__res import GetRecommendRes


@dataclass
class RecommendResult:
    products: list[tbls.ProductTable]

    def product_res(self) -> list[GetRecommendRes]:
        """
        RecommendResult内のproductsをGetRecommendResのリストに変換
        """
        return [
            GetRecommendRes(
                product_id=product.product_id,
                product_price=product.product_price,
                product_title=product.product_title,
                product_description=product.product_description,
                purchase_date=product.purchase_date,
                product_thumbnail_uuid=product.product_thumbnail_uuid,
                product_contents_uuid=product.product_contents_uuid,
            )
            for product in self.products
        ]
