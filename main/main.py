from data.api.elasticsearch_connector import add_news
from data.model.news import News, NewsMeta, SingleAnalysisResult
from features.simple_tag_extraction.main import SimpleTagExtractor
from features.spam_detection.rule_based_spam_extractor import spam


class NewsAnalyzer:
    def __init__(self, news: News):
        self.news = news
        self.analysis = SingleAnalysisResult()

    def analyze(self) -> SingleAnalysisResult:
        self.__index_elastic_search()
        self.__spam_detection()
        self.__summarize__()
        self.__tags_extraction()
        return self.analysis

    def __summarize__(self):
        ...
        # self.analysis.summary = "test"

    def __spam_detection(self):
        res = spam(self.news)
        self.analysis.spam_marks = [res]

    def __index_elastic_search(self):
        # add_news(self.news)
        ...

    def __tags_extraction(self):
        tags = SimpleTagExtractor(self.news).extract()
        self.analysis.tags = tags


class NewsIndexer:
    def __init__(self, news: News):
        self.news = news

    def index(self) -> dict:
        return self.__index_elastic_search()

    def __index_elastic_search(self):
        return add_news(self.news)

if __name__ == "__main__":
    pass
