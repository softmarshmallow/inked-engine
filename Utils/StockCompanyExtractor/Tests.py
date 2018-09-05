from datetime import datetime



def AhoCorasickTest():
    from Utils.StockCompanyExtractor.StockCompanyExtractor import FindAllCompanyInContent
    st = datetime.now()

    from Api.LocalJsonDatabaseService import GetLocalNewsData

    newsDataList = GetLocalNewsData(max=100, hasMaxValue=True)
    i = 0
    for newsData in newsDataList:
        print(i)
        # compList = FindAllCompanyInContent_LOOP(newsData)
        compList = FindAllCompanyInContent(newsData.get_news_content())
        i += 1
        et = datetime.now()
        print(compList)
        print("operation took...", (et - st))

