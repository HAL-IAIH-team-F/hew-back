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

        # [
        #     GetRecommendRes(
        #         product_id="123",
        #         product_title="Product A",
        #         product_thumbnail_uuid="abc",
        #         product_contents_uuid="def",
        #         product_price=1000,
        #         product_description="This is Product A",
        #         product_date="2024-01-01"
        #     ),
        #     GetRecommendRes(
        #         product_id="456",
        #         product_title="Product B",
        #         product_thumbnail_uuid="xyz",
        #         product_contents_uuid="uvw",
        #         product_price=2000,
        #         product_description="This is Product B",
        #         product_date="2024-02-01"
        #     )
        # ]

