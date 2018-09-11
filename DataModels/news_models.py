from datetime import datetime
from typing import List

from DataModels.models import ProductModel, PersonModel, QuantityModel, IncidentModel, CompanyModel


class NewsDataModel(object):
    """docstring for NewsModel"""

    def __init__(self, id, newsTitle, newsContent, newsTime, providerId, compTags):
        super(NewsDataModel, self).__init__()
        self.id = id
        self.newsTitle: str = newsTitle
        self.newsContent: str = newsContent
        self.newsTime: datetime = newsTime
        self.providerId = providerId
        self.mentionedCompanies: List[str]
        self.language = 'ko'
        self.category = 'undefined'

    def __str__(self):
        return '''
NewsDataModel: {}
Title:: {}
Time:: {}
Body:: 
{}
        '''.format(id(self), self.newsTitle, self.newsTime, self.get_news_content()[:100])

    def __repr__(self):
        return self.__str__()

    def get_news_content(self, removeHtml=True, removeAdSection=True, removeNewLine=True):
        self._newsContent = ""

        if removeAdSection:
            from Utils.AdRemover.AdSectionRemover import GetAdLessContent
            self._newsContent = GetAdLessContent(self.newsContent)

        if removeHtml:
            from bs4 import BeautifulSoup
            bs = BeautifulSoup(self._newsContent, 'lxml')
            self._newsContent = bs.getText()

        # remove '\r'
        if removeNewLine:
            # self._newsContent = self._newsContent.replace('\r', ' ')
            self._newsContent = self._newsContent.replace('\n', ' ')

        return self._newsContent

    # FIXME
    @property
    def mentionedCompanies(self):
        return self.__newsCompTags

    # FIXME
    @mentionedCompanies.setter
    def mentionedCompanies(self, val: List[str]):
        from Api.NewsDataService import NewsDataService

        self.__newsCompTags = val
        # update record


@DeprecationWarning
def CreateNewNewsModelFromJson(newsJson):
    id = newsJson.key
    newsTitle = newsJson["newsTitle"]
    newsContent = newsJson["newsContent"]
    newsTime = newsJson["newsTime"]
    providerId = newsJson["providerId"]
    # relatedCompanyCodes = newsJson["relatedCompanyCodes"]

    newNewsData = NewsDataModel(id, newsTitle, newsContent, newsTime, providerId)
    return newNewsData


def CreateNewNewsModelFromJson_MongoDB(newsDict: dict):
    id = newsDict["_id"]
    newsTitle = newsDict["title"]
    newsContent = newsDict["content"]
    newsTime = newsDict["time"]
    providerId = newsDict["providerID"]

    # FIXME
    # try:
    #     compTags = newsDict["compTags"]
    # except KeyError:
    #     compTags = []
    compTags = None
    newNewsData = NewsDataModel(id, newsTitle, newsContent, newsTime, providerId, compTags)
    return newNewsData


class AnalyzedNewsModel:
    def __init__(self, newsData: NewsDataModel, products:[ProductModel], peoples: [PersonModel], quantities: [QuantityModel], incidents: [IncidentModel], companies: [CompanyModel]):
        self.newsData = newsData
        self.products = products
        self.peoples = peoples
        self.quantities = quantities
        self.incidents = incidents
        self.companies = companies

    def __str__(self):
        return \
"""
companies: [{}]""".format(
    # products: [{}]
    # ''.join([str(p) for p in self.products]),
    ''.join([str(c) for c in self.companies])
)

    def __repr__(self):
        return self.__str__()


