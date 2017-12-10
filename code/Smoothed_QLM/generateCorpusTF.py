import pickle
import sys

corpus = pickle.load(open("corpus.p", "rb"));

tf = {}

for doc in corpus:
    sys.stdout.write(".");
    for word in corpus[doc]:
        if word in tf:
            tf[word] += 1;
        else:
            tf[word] = 1;


pickle_out = open("collectionTF.p","wb")
pickle.dump(tf, pickle_out)
pickle_out.close()
