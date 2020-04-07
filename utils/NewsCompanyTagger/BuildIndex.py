from data.api import NewsDataService
from NamedEntityRecognition.krx_company.company_extractor import \
    find_companies_in_content
from data.local.models import CompanyModel


@DeprecationWarning
class NewsCompanyIndexBuilder:
    """
    뉴스 데이터에대한 종목정보를 태깅하여 미리 저장해둠.
    NewsID : [CompCode]
    """

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
            comp_infos:[CompanyModel] = find_companies_in_content(newsData.get_news_content(), allow_overlap=False)
            comp_codes = [i.information.compCode for i in comp_infos]
            # Save here
            NewsDataService().SetCompTags(newsData.id, comp_codes)

            if i % 1000 == 0:
                print(i, "Done", allCnt - i, "Left")
            i += 1
        print("Operation Compete! \nin doers we trust..")


if __name__ == "__main__":
    NewsCompanyIndexBuilder(testRun=False)
