
# All News
from Api.NewsDataService import NewsDataService
from Utils.StockCompanyExtractor.StockCompanyExtractor import FindAllCompanyInContent


service = NewsDataService()
AllNews = service.FetchNewsData()

i = 0
for news in AllNews:
    comps = FindAllCompanyInContent(news)
    # print(news.newsTitle, comps)
    tags = [t[0] for t in comps]
    # print(tags)
    service.SetCompTags(news.id, tags)
    i += 1
    print(i)
