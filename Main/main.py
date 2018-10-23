import time
from pprint import pprint
from threading import Thread

from Api.NewsDataService import NewsDataService
from DataModels.news_models import AnalyzedNewsModel, NewsDataModel
from Utils.SentTokenizer import sent_tokenize
from NamedEntityRecognition.IncidentExtraction.incedent_extractor import IncidentExtractor
from NamedEntityRecognition.StockCompanyExtractor.StockCompanyExtractor import CompanyExtractor
from NamedEntityRecognition.QuantityExtraction.quantity_extractor import QuantityExtractor
from NamedEntityRecognition.PeopleExtraction.people_extractor import PeopleExtractor
from NamedEntityRecognition.ProductExtraction.product_extraction import ProductExtractor

from multiprocessing.dummy import Pool as ThreadPool

# MAIN PROCESSING DATA
UNPROCESSED_CRAWLED_DATA_POOL = []

# ANALYZED DATA
ANALYSIS_COMPLETE_POOL = []


THREAD_COUNT = 4

DO_LISTEN_TO_CRAWLER = True

def main():
    ConstantAnalysisHelper().start()
    print("joined")
    ...


class ConstantAnalysisHelper(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:

            if len(UNPROCESSED_CRAWLED_DATA_POOL) > 0:
                pool = ThreadPool(THREAD_COUNT)
                pool.starmap(analyze, UNPROCESSED_CRAWLED_DATA_POOL)
                # close the pool and wait for the work to finish
                pool.close()
                pool.join()
                print("pool joined")
            time.sleep(0.1)


def listen_to_crawler():
    import Main.crawler_listener.crawler_listener as l
    l.run_threaded()
    l.callback = add_item


def add_item(crawled_data):
    UNPROCESSED_CRAWLED_DATA_POOL.append(crawled_data)
    print("UNPROCESSED_CRAWLED_DATA_POOL:: ", len(UNPROCESSED_CRAWLED_DATA_POOL))


def analyze(news_data: NewsDataModel):
    print("start analysis")
    # split sentences
    sents = sent_tokenize(news_data.newsContent, module='nltk')
    # pprint(sents)

    analized = []
    for sent in sents:
        incidents = IncidentExtractor(sent).extract_incidents()
        companies = CompanyExtractor(sent).extract_companies()
        quantities = QuantityExtractor(sent).extract_most_informative()
        peoples = PeopleExtractor(sent).extract_peoples()
        products = ProductExtractor(sent).extract_products()

        result = AnalyzedNewsModel(
            newsData=news_data,
            incidents=incidents,
            companies=companies,
            quantities=quantities,
            peoples=peoples,
            products=products
        )

        analized.append(result)

    return analized



def test():
    news_data_list = NewsDataService().FetchNewsData(10)
    for news_data in news_data_list:
        result = analyze(news_data)
        print(result)


if __name__ == "__main__":
    main()
    if DO_LISTEN_TO_CRAWLER:
        listen_to_crawler()
