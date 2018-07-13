from typing import List


class NewsDataModel(object):

    """docstring for NewsModel"""
    def __init__(self, id, newsTitle, newsContent, newsTime, providerId, compTags):
        super(NewsDataModel, self).__init__()
        self.id = id
        self.newsTitle = newsTitle
        self.newsContent = newsContent
        self.newsTime = newsTime
        self.providerId = providerId
        # FIXME
        self.newsCompTags: List[str] #= compTags

    def __str__(self):
        return self.newsTitle

    def get_newsContent(self, removeHtml=True, removeAdSection=True):
        self._newsContent = ""
        if removeAdSection:
            from Utils.AdRemover.AdSectionRemover import GetAdLessContent
            self._newsContent = GetAdLessContent(self.newsContent)

        if removeHtml:
            from bs4 import BeautifulSoup
            bs = BeautifulSoup(self._newsContent, 'lxml')
            self._newsContent = bs.getText()

        return self._newsContent


    # FIXME
    @property
    def newsCompTags(self):
        return self.__newsCompTags

    # FIXME
    @newsCompTags.setter
    def newsCompTags(self, val: List[str]):
        from Api.NewsDataService import NewsDataService

        self.__newsCompTags = val
        # update record
        NewsDataService().SetCompTags(self.id, val)


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


def CreateNewNewsModelFromJson_MongoDB(newsDict:dict):
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


