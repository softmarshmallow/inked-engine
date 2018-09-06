
from Api.ProductDataService import ProductDataService

service = ProductDataService()

products = service.FetchAllProduct()

print(products)
