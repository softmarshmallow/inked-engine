import numpy as np
import pandas as pd
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import matplotlib.pyplot as plt
from Api.LocalJsonDatabaseService import GetLocalNewsData

cvec = CountVectorizer(min_df=1, max_df=.5, ngram_range=(1, 2))


# Calculate all the n-grams found in all documents
from itertools import islice


newsDataList = GetLocalNewsData(max=1, hasMaxValue=True)
newsData = newsDataList[0]

twitter = Twitter()
l = twitter.pos(newsData.newsContent)
words = [i[0] for i in l]

cvec.fit(words)
len = len(cvec.vocabulary_)
print(len)

a = list(islice(cvec.vocabulary_.items(), 20))
print(a)


cvec_counts = cvec.transform(words)
occ = np.asarray(cvec_counts.sum(axis=0)).ravel().tolist()
counts_df = pd.DataFrame({'term': cvec.get_feature_names(), 'occurrences': occ})
top = counts_df.sort_values(by='occurrences', ascending=False)


print(top)







from sklearn.feature_extraction.text import TfidfVectorizer
# list of text documents
text = ["The quick brown fox jumped over the lazy dog.",
        "The dog.",
        "The fox"]
# create the transform
vectorizer = TfidfVectorizer()
# tokenize and build vocab
vectorizer.fit(text)
# summarize
print(vectorizer.vocabulary_)
print(vectorizer.idf_)
# encode document
vector = vectorizer.transform([text[0]])
# summarize encoded vector
print(vector.shape)
print(vector.toarray())