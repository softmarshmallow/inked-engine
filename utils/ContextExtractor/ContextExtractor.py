from data.api.NewsDataService import NewsDataService
from utils.SentTokenizer import sent_tokenize
from NamedEntityRecognition.StockCompanyExtractor.StockCompanyExtractor import FindAllCompanyInContent

#  Load news
newsList = NewsDataService().FetchNewsData(100)
for newsData in newsList:
    print("\n\n")
    sentences = sent_tokenize(newsData.get_news_content())

    last_section_comps = []

    for sent in sentences:

        comps = FindAllCompanyInContent(sent)
        if len(comps) > 0:
            if last_section_comps == comps:
                print("\n\n")
                print("Match")
            else:
                print("Mis match")
                pass
            last_section_comps = comps
            # pprint(comps)
        print(comps, sent)


# 1 모든 종목 추출

# 2 종목 split

#
