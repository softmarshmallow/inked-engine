import csv
from pprint import pprint
from typing import List

import os

from conf import DATA_SOURCE_ROOT
from data.local.models import CompanyModel

companies: List[CompanyModel] = None


def GetCompWithName(compName) -> CompanyModel:
    """
    :param compName: "삼성전자"
    :return: Comp(000244)
    """
    for comp in FetchAllCompanyList():  # for name, age in list.items():  (for Python 3.x)
        if comp.compName == compName:
            return comp


# region Utils
def PolishCompCode(rawCompCode) -> str:
    '''
    converts n digit(s) to 6 filled digits

    :param rawCompCode: 889
    :return: 00889
    '''
    return str(rawCompCode).zfill(6)


# def CompNameToCompTuple(compName) -> tuple:
#     return GetCompCodeWithName(compName), compName

# endregion


def FetchAllCompanyList() -> List[CompanyModel]:
    global companies
    if companies is not None:
        return companies

    companies = []

    filename = os.path.join(DATA_SOURCE_ROOT, "KRX-Stock/KRX-Stock-List.csv")
    file = open(filename, "r")
    reader = csv.reader(file)
    # Skip Header
    next(reader, None)
    for row in reader:
        # row[0] = CompCode
        # row[1] = CompName
        compCode = PolishCompCode(row[0])
        compName = row[1]
        newCompObj = CompanyModel(compName, compCode)
        companies.append(newCompObj)
    return companies


def FetchAllCompName() -> List[str]:
    compList: List[CompanyModel] = FetchAllCompanyList()
    return [c.compName for c in compList]


def FetchAllCompCode() -> List[str]:
    compList: List[CompanyModel] = FetchAllCompanyList()
    return [c.compCode for c in compList]



if __name__ == "__main__":
    l = FetchAllCompanyList()
    pprint(l)
    print(len(l))