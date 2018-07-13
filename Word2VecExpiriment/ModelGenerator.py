from gensim.models import word2vec


def TrainModel(inputFile:str, outputModelPath):
    print("start w2v model training...")
    data = word2vec.Text8Corpus(inputFile)
    model = word2vec.Word2Vec(data, size=100)
    model.save(outputModelPath)
    print("Completed ! ")


if __name__ == "__main__":
    TrainModel("Corpus/NewsContent.corpus", "W2V_Models/NewsContent.model")
    # TrainModel("Corpus/NewsTitle.corpus", "W2V_Models/NewsTitle.model")
    # TrainModel("Corpus/Wiki.corpus", "W2V_Models/Wiki.model")
