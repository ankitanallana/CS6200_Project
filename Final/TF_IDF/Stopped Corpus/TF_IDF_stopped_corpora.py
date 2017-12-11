
# coding: utf-8

# ### All imports

# In[1]:


from tf_idf import *
from evaluation import *


# In[6]:


stop_words = [word.rstrip('\n') for word in open('common_words')]
# corpus_dict = generateCorpus("corpus", type="default")
corpus_dict = loadCorpus("corpus")
# stopped_corpus_dict = generateStoppedCorpus(corpus_dict, stop_words)
stopped_corpus_dict = loadCorpus("stopped_corpus")
print("corpus loaded")


# In[7]:


stopped_corpus_dict


# In[8]:


for doc, string in stopped_corpus_dict.items():
    words = string.split(" ")
    stopped_corpus_dict[doc] = words


# In[9]:


len(stopped_corpus_dict)
stopped_corpus_dict['CACM-1027']


# In[39]:


# full_corpus_dict = generateCorpus("full_corpus", type="sentence")
full_corpus_dict = loadCorpus("full_corpus")
print("full_corpus loaded")


# In[25]:


full_corpus_dict['CACM-0270']


# In[26]:


# Load term frequencies
unigrams_dict = generateUnigrams(stopped_corpus_dict)
print("Unigrams loaded")
len(unigrams_dict)
#unigrams_dict


# In[27]:


# Compute DF and IDF

df = generateDocumentFrequencies(stopped_corpus_dict)
print(len(df))
idf = calculateIDF(stopped_corpus_dict, df)
idf['algorithm']


# In[28]:


queries = retrieveQueries("cacm.query.txt")
i = 0
for query in queries:
    query = remove_punctuation(query.lower())
    query = query.split(" ")
    
    query = diff(query, stop_words)
    
    for q in query:
        if len(q)<1:
            query.remove(q)
    
    queries[i] = " ".join(query)
    i+=1


# In[29]:


results={}
count = 1
for query in queries:
    query_id = "q_"+str(count)
    print(query_id)
    results[query_id] = sortByScore(queryForResults(query, df, stopped_corpus_dict, idf))
    count+=1
    
print("Results generated for all queries")


# In[30]:


# Write Results to File

for query_id, query_result in results.items():
    print("Writing result to file "+query_id)
    writeResultsToFile(query_result, "_STOPPED_TF_IDF_"+query_id, query_id)


# In[ ]:


count = 1
for query in queries:
    query_id = "q_"+str(count)
    print(query_id)
    html_file = generateHTML(generateSnippets(results[query_id], full_corpus_dict, query), results[query_id], query)
    f = open("query_results_"+query_id+".html", "w+")
    f.write(html_file)
    f.close()
    count+=1
    #break
print("Snippets & HTML files generated")


# In[31]:


query_rel = {}


# In[32]:


query_rel = queryRelevance()


# In[33]:


relevance_set=generateRelevanceSet(query_rel, results)


# In[34]:


# Calculate MRR

mrr_output=calculateMRR(relevance_set)    
mrr_output
mrr_output_string=""
f=open("STOPPED_MRR_TF_IDF.txt", "w+")

for query, mrr_score in mrr_output.items():
    mrr_output_string+=query+" : "+str(mrr_score)+"\n"
f.write(mrr_output_string)
f.close()


# In[35]:


# Calculate P@K

f=open("STOPPED_P@K_TF_IDF.txt", "w+")
pAtKOutput=""
for query_id, rel_set in relevance_set.items():
    pAtKOutput+=query_id+"\n\n"
    K=5
    pAtKOutput+="K = "+str(K)+"\n"
    pAtKOutput+="Precision = "+str(precisionAtK(relevance_set, K, query_id))+"\n"
    
    K=20
    pAtKOutput+="K = "+str(K)+"\n"
    pAtKOutput+="Precision = "+str(precisionAtK(relevance_set, K, query_id))+"\n"
    pAtKOutput+="\n------------------\n\n"

f.write(pAtKOutput)
f.close()
print("P@K written to file")


# In[36]:


# Calculate Mean Average Precision (MAP)

f=open("STOPPED_MAP_TF_IDF.txt", "w+")
mapOutput="MAP SCORES FOR TF IDF \n\n"
    
for query_id in relevance_set.keys():
    mapOutput+=query_id+" : "+str(calculateMAP(relevance_set, query_id))+"\n"
    
f.write(mapOutput)
f.close()
print("MAP written to file")


# In[37]:


# Generate all precision tables
for query_id in relevance_set.keys():
    generateAllPrecisionTable(relevance_set, query_id)


# In[38]:


# Generate full Recall tables

for query_id in relevance_set.keys():
    generateRecallTable(relevance_set, query_id)

