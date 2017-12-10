
# coding: utf-8

# ### All imports

# In[1]:


from tf_idf import *
from evaluation import *


# In[2]:


stemmed_corpus = loadStemmedCorpus("cacm_stem.txt")
print("corpus loaded")


# In[3]:


for doc, string in stemmed_corpus.items():
    words = string[0].split(" ")
    stemmed_corpus[doc] = words
print(len(stemmed_corpus))


# In[6]:


# Load term frequencies
unigrams_dict = generateUnigrams(stemmed_corpus)
print("Term Frequencies generated")


# In[8]:


# Compute DF and IDF

df = generateDocumentFrequencies(stemmed_corpus)
print("Document Frequencies generated")

idf = calculateIDF(stemmed_corpus, df)
print("IDFs computed")


# In[10]:


queries=[]
with open("cacm_stem.query.txt") as f:
        queries.append(f.readlines())

queries = queries[0]

for i, query in enumerate(queries):
    queries[i]=query.strip()
print("Stemmed queries : \n"+str(queries))


# In[11]:


results={}
count = 1
print("Will now rank documents per query using TF-IDF")
for query in queries:
    query_id = "q_"+str(count)
    print(query_id)
    results[query_id] = sortByScore(queryForResults(query, df, stemmed_corpus, idf))
    count+=1
    
print("Results generated for all queries")


# In[12]:


# Write Results to File

for query_id, query_result in results.items():
    print("Writing result to file "+query_id)
    writeResultsToFile(query_result, "_STEMMED_TF_IDF_"+query_id, query_id)

