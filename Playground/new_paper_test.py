from newspaper import Article
url = 'https://news.naver.com/main/ranking/read.nhn?mid=etc&sid1=111&rankingType=popular_day&oid=277&aid=0004308735&date=20180904&type=1&rankingSeq=9&rankingSectionId=100'
article = Article(url, language='ko')
article.download()
article.parse()
print(article.html)
print(article.publish_date)
print(article.nlp())
