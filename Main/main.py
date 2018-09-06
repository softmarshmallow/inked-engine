from pprint import pprint

from Api.misc.naver_news_data_service import get_article_content_list
from Utils.SentTokenizer import sent_tokenize



def analyze(news):
    # split sentences
    sents = sent_tokenize(article_body, module='nltk')
    pprint(sents)


if __name__ == "__main__":
    for article_body in get_article_content_list(max=10):
        analyze(article_body)


