
class CompanyModel(object):
    def __init__(self, compName, compCode):
        self.compName = compName
        self.compCode = compCode

    def __str__(self):
        return self.compCode + ":" + self.compName
