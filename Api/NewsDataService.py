from typing import List

from bson import ObjectId

from DataModels.NewsDataModel import NewsDataModel, CreateNewNewsModelFromJson_MongoDB
from pymongo import MongoClient


class NewsDataService:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.inked_news_storage
        self.newsTable = self.db.news

    def FetchNewsData(self, cnt: int = None) -> List[NewsDataModel]:
        fetchedList = []

        q = self.newsTable.find()
        if cnt is not None:
            q.limit(cnt)

        for document in q:
            newsData = CreateNewNewsModelFromJson_MongoDB(document)
            fetchedList.append(newsData)

        return fetchedList

    def WriteNewsData(self, newsData: NewsDataModel):
        pass

    def SetCompTags(self, newsDataID: str, compTags: List[str]):
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


# Temporary method
# 로컬 데이터를 디비로 옮길때 사용, 아키텍쳐 변경시 deprecated.
def SetupDB():
    from Api.LocalJsonDatabaseService import GetLocalNewsData

    ask = input("this action will override all DB.... (Y/N)")
    if ask != "Y":
        return

    client = MongoClient('localhost', 27017)
    db = client.inked_news_storage
    newsTable = db.news
    newsTable.drop()

    all_newsData = GetLocalNewsData(hasMaxValue=False)
    total = len(all_newsData)
    i = 0
    for newsData in all_newsData:
        news_data = {
            'title': newsData.newsTitle,
            'content': newsData.newsContent,
            'time': newsData.newsTime,
            'providerID': newsData.providerId
        }
        result = newsTable.insert_one(news_data)
        print('One post: {0}'.format(result.inserted_id))
        print("TOTAL", total, "DONE", str(i))
        i += 1


if __name__ == "__main__":
    # c = NewsDataService()
    # l = c.FetchNewsData(10)
    from Utils.StockCompanyExtractor.StockCompanyExtractor import CompNameToCompTuple

    c = CompNameToCompTuple("삼성전자")
    l = NewsDataService().FetchCompNews(c)
    for i in l:
        print(type(i))
        print(i)
        print(i.id)
