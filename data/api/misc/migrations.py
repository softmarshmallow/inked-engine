from Utils.NewsCompanyTagger.BuildIndex import NewsCompanyIndexBuilder


def MigrateToDatabase_NaverNewsDump():
    """
    news.naver.com // inkednewscrawler 통해 수집한 뉴스 데이터를 바탕으로 디비를 구성합니다.
    로컬 데이터를 디비로 옮길때 사용, 아키텍쳐 변경시 deprecated.

    :return:
    """
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.inked_news_storage_navernews
    newsTable = db.news
    newsTable.drop()

    from data.api import get_all_article_detail_list
    all_articles = get_all_article_detail_list()
    total = len(all_articles)
    i = 0
    print("total", total)
    for article in all_articles:
        news_data = {
            'title': article["title"],
            'content': article["body_html"],
            'time': article["time"],
            'providerID': article["provider"]
        }
        result = newsTable.insert_one(news_data)
        # print('One post: {0}'.format(result.inserted_id))
        print("TOTAL", total, "DONE", str(i))
        i += 1

def MigrateToDatabase_FirebaseDump():
    """
    Evil-eye firebase. json을 mongo db 로 migrate 한다.
    Temporary method
    로컬 데이터를 디비로 옮길때 사용, 아키텍쳐 변경시 deprecated.
    """



    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.inked_news_storage
    newsTable = db.news
    newsTable.drop()

    from data.api import GetLocalNewsData
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
    print('''
    ====================DB_GEN_V_0.0.0======================
    This action is only required when creating new database Via local data.
    Please read this documentation, reconsider using this operation.
    ===========================================================
    ''')

    option = input("What operation to use? (ebest, naver)")
    ask = input("this action will override all DB.... (Y/N)")
    if ask != "Y":
        quit()
    if option == "ebest":
        DEFAULT_NEWS_DATABASE = 'ebest'
        MigrateToDatabase_FirebaseDump()
    elif option == "naver":
        DEFAULT_NEWS_DATABASE = 'naver'
        MigrateToDatabase_NaverNewsDump()

    # Seed database
    # Eg. process mentioned company

    print("Migration Completed")

    NewsCompanyIndexBuilder()
