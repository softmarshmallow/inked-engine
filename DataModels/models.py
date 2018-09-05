
class CompanyModel(object):
    def __init__(self, compName, compCode):
        self.compName = compName
        self.compCode = compCode

    def __str__(self):
        return self.compCode + ":" + self.compName

    def __repr__(self):
        return self.__str__()


class ExtractedInformation:
    def __init__(self, original: object, information: object, index: int):
        self.original = original
        self.information = information
        self.index = index