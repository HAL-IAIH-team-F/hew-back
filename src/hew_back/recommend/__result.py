from dataclasses import dataclass

from sqlalchemy import Sequence

from hew_back import tbls
from hew_back.recommend.__res import GetRecommendRes, ProductRes


@dataclass
class RecommendResult:
    products: Sequence[tbls.ProductTable]

    def products_res(self) -> GetRecommendRes:
        """レスポンス形式に変換"""
        result: list[GetRecommendRes] = []
        for product in self.products:
            result.append(product.to_product_res())
        return GetRecommendRes.create(result)
