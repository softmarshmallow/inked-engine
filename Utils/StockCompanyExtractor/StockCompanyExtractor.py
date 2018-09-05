import ahocorasick
from typing import List

from Api.CompanyDataService import FetchAllCompName, GetCompWithName, FetchAllCompanyList
from Api.NewsDataService import NewsDataService
from DataModels.models import CompanyModel
from DataModels.news_models import NewsDataModel

compList: List[CompanyModel] = None


def FindAllCompanyInContent_LOOP(news: NewsDataModel) -> List[str]:
    """Finds company in news, but with loop method."""
    includedCompList = []
    for compName in FetchAllCompName():
        if compName in news.get_news_content():
            includedCompList.append(compName)

    return includedCompList


def FindAllCompanyInContent(content: str, allowOverlap: bool = True) -> List[CompanyModel]:
    """
    Finds company in news, but with Aho corasic method
    allowOverlap = True // 삼성전자, 대성, 삼성전자, 삼성전자 || False // 삼성전자, 대성"""
    companies: List[CompanyModel] = []

    auto = ahocorasick.Automaton()
    for comp in FetchAllCompanyList():
        auto.add_word(comp.compName, comp.compName)
    auto.make_automaton()

    for found in auto.iter(content):
        filtered_compName = found[1]
        companies.append(GetCompWithName(filtered_compName))
        # print(found)

    if not allowOverlap:
        no_overlap_comps = []
        [no_overlap_comps.append(v) for v in companies if v not in no_overlap_comps]
        return no_overlap_comps

    return companies


def FindAllNewsContainsCompany(compCode) -> List[NewsDataModel]:
    """
    미리 태깅하여 저장한 종목 정보로 뉴스를 조회함.
    해당 종목이 포함된 뉴스를 반환함.
    """
    return NewsDataService().FetchCompNews(compCode)


if __name__ == "__main__":
    a = FetchAllCompanyList()
    print(a)
    for b in a:
        print(b)
    print(GetCompWithName("삼성전자"))

    allComp = FetchAllCompanyList()
    for comp in allComp:
        FindAllNewsContainsCompany(comp.compCode)

