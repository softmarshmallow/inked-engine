from datetime import datetime
from konlpy.tag import Mecab
from data.api import get_title_list


mecab = Mecab()

sents = get_title_list(start_date=datetime(2018, 1, 1), end_date=datetime(2018, 1, 1))

sents = sents[:100]
for sent in sents:
    tagged = mecab.pos(sent)
    print(sent)
    print(tagged)
