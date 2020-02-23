
from data.api import ProductDataService

service = ProductDataService()

products = service.FetchAllProduct()

print(products)


class ProductExtractor:
    def __init__(self, txt):
        self.txt = txt

    def extract_products(self):
        ...

