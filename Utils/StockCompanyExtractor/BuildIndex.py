from Api.NewsDataService import NewsDataService
from Utils.StockCompanyExtractor.StockCompanyExtractor import FindAllCompanyInContent


# 뉴스 데이터에대한 종목정보를 태깅하여 미리 저장해둠.
# NewsID : [CompCode]
class NewsCompanyIndexBuilder:
    def __init__(self, testRun=True):
        self.testRun = testRun
        self.TagArticles()

    def TagArticles(self):
        if self.testRun:
            allNewsData = NewsDataService().FetchNewsData(cnt=1)
        else:
            allNewsData = NewsDataService().FetchNewsData()

        allCnt = len(allNewsData)
        print("TagArticles for", allCnt, "articles")
        i = 1
        for newsData in allNewsData:
            comps = FindAllCompanyInContent(newsData, allowOverlap=False)
            # compCodes = [i[0] for i in comps]
            newsData.newsCompTags = comps
            if i % 1000 == 0:
                print(i, "Done", allCnt - i, "Left")
            i += 1
        print("Operation Compete! \nin doers we trust..")


if __name__ == "__main__":
    NewsCompanyIndexBuilder(testRun=False)
