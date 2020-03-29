from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

exampleSentence = "This is an example showing off stop word filtration."
stopWords = set(stopwords.words("english"))

print(stopWords)

words = word_tokenize(exampleSentence)

# filteredSentence = []
# for w in words:
#     if w not in stopWords:
#         filteredSentence.append(w)
filteredSentence = [w for w in words if not w in stopWords]


print(filteredSentence)
