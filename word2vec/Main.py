from typing import List
from gensim.models import word2vec
import pprint


# Model:    NewsTitle, NewsContent, Wiki

def RunWord2Vec(query: List, model: str = "NewsContent"):
    path = "W2V_Models/" + model + ".model"
    model = word2vec.Word2Vec.load(path)
    return model.most_similar(positive=query)


if __name__ == "__main__":
    result = RunWord2Vec(["TIGER"], model="NewsContent")
    pprint.pprint(result)
