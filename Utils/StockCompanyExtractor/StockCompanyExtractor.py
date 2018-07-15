import ahocorasick
import csv
from typing import List

from datetime import datetime

import os

from Api.NewsDataService import NewsDataService
from DataModels.NewsDataModel import NewsDataModel


# region Utils

# 889 -> 00889
def PolishCompCode(rawCompCode) -> str:
    return str(rawCompCode).zfill(6)


def CompNameToCompTuple(compName) -> tuple:
    return GetCompCodeWithName(compName), compName


# endregion


compDict: dict = None


def FetchAllCompanyName() -> dict:
    global compDict
    if compDict is not None:
        return compDict

    compDict = {}
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
        compDict[compCode] = compName
    return compDict


def FetchAllCompName() -> List[str]:
    compDict: dict = FetchAllCompanyName()
    compNameList = list(compDict.values())
    return compNameList


def FindAllCompanyInContent_LOOP(news: NewsDataModel) -> List[str]:
    includedCompList = []
    for compName in FetchAllCompName():
        if compName in news.get_newsContent():
            includedCompList.append(compName)

    return includedCompList


# allowOverlap = True // 삼성전자, 대성, 삼성전자, 삼성전자 || False // 삼성전자, 대성
def FindAllCompanyInContent(news: NewsDataModel, allowOverlap: bool = True) -> List[tuple]:
    companies: List[tuple] = []

    listStrings = news.get_newsContent()
    auto = ahocorasick.Automaton()
    for compName in FetchAllCompName():
        auto.add_word(compName, compName)
    auto.make_automaton()

    # for astr in listStrings:
    # print(newsData.newsTitle)
    for a in auto.iter(listStrings):
        filtered_compName = a[1]
        companies.append((GetCompCodeWithName(filtered_compName), filtered_compName))
        # print(a)

    if not allowOverlap:
        no_overlap_comps = []
        [no_overlap_comps.append(v) for v in companies if v not in no_overlap_comps]
        return no_overlap_comps

    return companies


def GetCompCodeWithName(compName) -> str:
    for code, name in FetchAllCompanyName().items():  # for name, age in list.items():  (for Python 3.x)
        if name == compName:
            return code


# Improvements 미리 모든뉴스 테깅후 DB저장, DB에서 추출.
def FindAllNewsContainsCompany(comp) -> List[NewsDataModel]:
    return NewsDataService().FetchCompNews(comp)


if __name__ == "__main__":
    allComp = FetchAllCompanyName()
    for comp in allComp.items():
        FindAllNewsContainsCompany(comp)

