

# Twitter
from konlpy.tag import Twitter
# EX. 삼성전자를 삼성과 전자로 분류하는 오류..
sent = "삼성전자 주식 대박친다. 대우전자는 바닥친다."
twitter = Twitter()
malist = twitter.pos(sent, norm=True, stem=True)
print(malist)


# Mecab
from konlpy.tag import Mecab
mecab = Mecab()
malist = mecab.pos(sent)
print(malist)
