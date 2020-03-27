from nltk import ngrams
import pprint
sentence = 'this is a foo bar sentences and i want to ngramize it'
n = 2
ngrams = ngrams(sentence.split(), n)


# pprint.pprint(ngrams)
for grams in ngrams:
    print (grams)