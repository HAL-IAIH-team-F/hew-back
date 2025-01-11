from dataclasses import dataclass

from hew_back import tbls


@dataclass
class ProductsResult:
    products: list[tbls.ProductTable]
