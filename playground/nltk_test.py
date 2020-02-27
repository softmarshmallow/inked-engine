from nltk.corpus import gutenberg
from nltk.tokenize import PunktSentenceTokenizer
import nltk
raw = gutenberg.raw('melville-moby_dick.txt')

print(raw)
# Quantity Test


sents =  nltk.sent_tokenize(raw)

for sent in sents:
    print(sent)
    words = nltk.word_tokenize(sent)
    tagged = nltk.pos_tag(words)
    ne_tagged = nltk.ne_chunk(tagged)
    s = ne_tagged.subtrees()
    for i in s:
        print(i)



