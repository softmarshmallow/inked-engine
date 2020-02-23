from datetime import datetime
from typing import List


class IncidentModel(object):
    def __init__(self, name, type, relation):
        self.name = name
        self.type = type
        self.relation = relation

class PersonModel:
    def __init__(self, id, name, relations):
        self.id = id
        self.name = name
        self.relations = relations

    def __str__(self):
        return self.name

class CompanyModel(object):
    def __init__(self, compName, compCode):
        self.id = compCode
        self.compCode = compCode
        self.compName = compName

    def __str__(self):
        return self.compCode + ":" + self.compName

    def __repr__(self):
        return self.__str__()

class ProductModel:
    def __init__(self, id, productName, publishDate, company, category, tags):
        self.id = id
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
    def __init__(self, original: object, information: object, span: (int, int)):
        self.original = original # ex. text
        self.information = information # ex. company from text
        self.span: (int, int) = span # index

    def __str__(self):
        return "EI: [info]{} [span]{}".format(self.information, self.span)

    def __repr__(self):
        return self.__str__()
