from typing import List

import pymongo
from bson import ObjectId

from pymongo import MongoClient
import warnings

from conf import DEFAULT_NEWS_DATABASE
from data.local.models import CompanyModel
from data.local.news_models import NewsDataModel, CreateNewNewsModelFromJson_MongoDB


class NewsDataService:
    """
    source : ebest/naver
    """
    def __init__(self, source=None):
        self.client = MongoClient('localhost', 27017)

        if source is None: # if source parameter not setted, read from settings.
            source = DEFAULT_NEWS_DATABASE
        if source == 'ebest':
            self.db = self.client.inked_news_storage
        elif source == 'naver':
            self.db = self.client['inked-content-db']
        else:
            warnings.warn("wrong source input... please check :: ", source)
            self.db = self.client.inked_news_storage

        self.newsTable = self.db.raw

    def FetchNewsData(self, cnt: int = None, date_sort=-1) -> List[NewsDataModel]:
        fetchedList = []

        q = self.newsTable.find().sort('time', pymongo.DESCENDING)
        if cnt is not None:
            q.limit(cnt)

        for document in q:
            newsData = CreateNewNewsModelFromJson_MongoDB(document)
            fetchedList.append(newsData)

        return fetchedList

    def WriteNewsData(self, newsData: NewsDataModel):
        pass

    def SetCompTags(self, newsDataID: str, compTags: List[CompanyModel]):
        q = {"$set": {"compTags": compTags}}
        # q = {"$compTags": compTags}
        self.newsTable.update_one({"_id": ObjectId(newsDataID)}, q)

    def FetchCompNews(self, compCode) -> List:
        cursor = self.newsTable.find({"compTags": compCode})
        l = []
        for c in cursor:
            o = CreateNewNewsModelFromJson_MongoDB(c)
            l.append(o)
            # print(c)

        return l

    def FetchNewsWithKeyword(self, keyword):
        # TODO
        pass


if __name__ == "__main__":
    # c = NewsDataService()
    # l = c.FetchNewsData(10)
    from NamedEntityRecognition.krx_company import GetCompWithName

    c = GetCompWithName("삼성전자")
    l = NewsDataService().FetchCompNews(c)
    for i in l:
        print(type(i))
        print(i)
        print(i.id)
