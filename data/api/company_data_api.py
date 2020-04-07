import csv
from pprint import pprint
from typing import List

import os

from conf import DATA_SOURCE_ROOT
from data.local.models import CompanyModel

companies: List[CompanyModel] = None


def get_company_by_name(compName) -> CompanyModel:
    """
    :param compName: "삼성전자"
    :return: Comp(000244)
    """
    for comp in fetch_all_company_list():  # for name, age in list.items():  (for Python 3.x)
        if comp.compName == compName:
            return comp


# region Utils
def normalize_company_code(rawCompCode) -> str:
    '''
    converts n digit(s) to 6 filled digits

    :param rawCompCode: 889
    :return: 00889
    '''
    return str(rawCompCode).zfill(6)


def fetch_all_company_list() -> List[CompanyModel]:
    global companies
    if companies is not None:
        return companies

    companies = []

    filename = os.path.join(DATA_SOURCE_ROOT, "krx-company.csv")
    file = open(filename, "r")
    reader = csv.reader(file)
    # Skip Header
    next(reader, None)
    for row in reader:
        # row[1] = CompCode
        # row[2] = CompName
        compCode = normalize_company_code(row[1])
        compName = row[2]
        newCompObj = CompanyModel(compName, compCode)
        companies.append(newCompObj)
    return companies


def fetch_all_company_names() -> List[str]:
    compList: List[CompanyModel] = fetch_all_company_list()
    return [c.compName for c in compList]


def fetch_all_company_codes() -> List[str]:
    compList: List[CompanyModel] = fetch_all_company_list()
    return [c.compCode for c in compList]


if __name__ == "__main__":
    l = fetch_all_company_list()
    pprint(l)
    print(f"company total : {len(l)}")