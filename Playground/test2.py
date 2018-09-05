import pickle

path = "/Users/softmarshmallow/Downloads/annie-0.6/rsc/nusvc_model.pkl"


f = open(path, 'rb')
p = pickle.load(f)

print(p)



open('output.txt', 'w').write(str(p))