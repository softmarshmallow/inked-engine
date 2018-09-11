from pprint import pprint

from Api.NewsDataService import NewsDataService
from DataModels.news_models import AnalyzedNewsModel, NewsDataModel
from Utils.SentTokenizer import sent_tokenize
from NamedEntityRecognition.IncidentExtraction.incedent_extractor import IncidentExtractor
from NamedEntityRecognition.StockCompanyExtractor.StockCompanyExtractor import CompanyExtractor
from NamedEntityRecognition.QuantityExtraction.quantity_extractor import QuantityExtractor
from NamedEntityRecognition.PeopleExtraction.people_extractor import PeopleExtractor
from NamedEntityRecognition.ProductExtraction.product_extraction import ProductExtractor



def analyze(news_data: NewsDataModel):
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



if __name__ == "__main__":
    news_data_list = NewsDataService().FetchNewsData(10)
    for news_data in news_data_list:
        result = analyze(news_data)
        print(result)


