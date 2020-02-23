from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
exampleWords = ["python", "pythoner", "pythoning", "pythoned", "pythonly"]

for w in exampleWords:
    print(ps.stem(w))

# I was taking a ride in the car