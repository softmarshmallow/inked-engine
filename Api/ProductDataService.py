from typing import List

from settings import DATA_SOURCE_ROOT
from DataModels.models import ProductModel
import os
import json


class ProductDataService:
    def __init__(self):
        ...

    def FetchAllProduct(self) -> List[ProductModel]:
        file_path = os.path.join(DATA_SOURCE_ROOT, 'products_dictionary.json')
        with open(file_path) as f:
            data = json.load(fp=f)
        products = []
        for record in data:
            productName = record['product_name']
            pm = ProductModel(productName=productName, publishDate=None, company=None,
                              category=None, tags=None)
            products.append(pm)
        return products
