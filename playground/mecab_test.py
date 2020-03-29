from datetime import datetime
from konlpy.tag import Mecab
from data.api.content_db_connector import fetch_news_collection


mecab = Mecab()

docs = fetch_news_collection(time_from=datetime(2018, 1, 1), time_to=datetime(2018, 1, 1))
sents = [i.title for i in docs]
sents = sents[:100]
for sent in sents:
    tagged = mecab.pos(sent)
    print(sent)
    print(tagged)
