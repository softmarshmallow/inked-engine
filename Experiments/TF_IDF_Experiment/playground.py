from Experiments.TF_IDF_Experiment.tfidf import TfIdf




table = TfIdf()
table.add_document("foo", ["a", "b", "c", "d", "e", "f", "g", "h"])
table.add_document("bar", ["a", "b", "c", "i", "j", "k"])
table.add_document("baz", ["k", "l", "m", "n"])


a = table.similarities(["a", "b", "c"])
print(a)
