from datetime import datetime
from typing import List


class CompanyModel(object):
    def __init__(self, compName, compCode):
        self.compName = compName
        self.compCode = compCode

    def __str__(self):
        return self.compCode + ":" + self.compName

    def __repr__(self):
        return self.__str__()


class ProductModel:
    def __init__(self, productName, publishDate, company, category, tags):
        self.productName = productName
        self.company: CompanyModel = company
        self.publishDate: datetime = publishDate
        self.category = category
        self.tags: List[str] = tags

    def __str__(self):
        return "Product: {}".format(self.productName)

    def __repr__(self):
        return self.__str__()


class QuantityModel:
    def __init__(self, amount, unit, target):
        self.amount: float = amount
        self.unit: str = unit
        self.target: object = target


class ExtractedInformation:
    def __init__(self, original: object, information: object, index: int):
        self.original = original
        self.information = information
        self.index = index
