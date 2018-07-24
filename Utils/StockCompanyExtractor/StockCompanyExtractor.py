import ahocorasick
import csv
from typing import List

from datetime import datetime

import os

from Api.NewsDataService import NewsDataService
from DataModels.CompanyModel import CompanyModel
from DataModels.NewsDataModel import NewsDataModel


# TODO Move this as a service
# region Utils

# 889 -> 00889
def PolishCompCode(rawCompCode) -> str:
    return str(rawCompCode).zfill(6)


def CompNameToCompTuple(compName) -> tuple:
    return GetCompCodeWithName(compName), compName

# endregion


compList: List[CompanyModel] = None


def FetchAllCompanyList() -> List[CompanyModel]:
    global compList
    if compList is not None:
        return compList

    compList = []
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "KRX-Stock-List.csv")
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
        compList.append(newCompObj)
    return compList


def FetchAllCompName() -> List[str]:
    compList: List[CompanyModel] = FetchAllCompanyList()
    return [c.compName for c in compList]


def FetchAllCompCode() -> List[str]:
    compList: List[CompanyModel] = FetchAllCompanyList()
    return [c.compCode for c in compList]


def FindAllCompanyInContent_LOOP(news: NewsDataModel) -> List[str]:
    includedCompList = []
    for compName in FetchAllCompName():
        if compName in news.get_newsContent():
            includedCompList.append(compName)

    return includedCompList


# allowOverlap = True // 삼성전자, 대성, 삼성전자, 삼성전자 || False // 삼성전자, 대성
def FindAllCompanyInContent(news: NewsDataModel, allowOverlap: bool = True) -> List[tuple]:
    companies: List[tuple] = []

    content = news.get_newsContent()
    auto = ahocorasick.Automaton()
    for compName in FetchAllCompName():
        auto.add_word(compName, compName)
    auto.make_automaton()

    for found in auto.iter(content):
        filtered_compName = found[1]
        companies.append((GetCompCodeWithName(filtered_compName), filtered_compName))
        # print(found)

    if not allowOverlap:
        no_overlap_comps = []
        [no_overlap_comps.append(v) for v in companies if v not in no_overlap_comps]
        return no_overlap_comps

    return companies


def GetCompCodeWithName(compName) -> str:
    for comp in FetchAllCompanyList():  # for name, age in list.items():  (for Python 3.x)
        if comp.compName == compName:
            return comp.compCode


# Improvements 미리 모든뉴스 테깅후 DB저장, DB에서 추출.
def FindAllNewsContainsCompany(compCode) -> List[NewsDataModel]:
    return NewsDataService().FetchCompNews(compCode)


if __name__ == "__main__":
    a = FetchAllCompanyList()
    print(a)
    for b in a:
        print(b)
    print(CompNameToCompTuple("삼성전자"))

    allComp = FetchAllCompanyList()
    for comp in allComp:
        FindAllNewsContainsCompany(comp.compCode)

