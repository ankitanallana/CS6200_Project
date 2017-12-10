
# coding: utf-8

# ### All imports

# In[10]:


from tf_idf import *
from evaluation import *


# In[11]:


corpus_dict = generateCorpus("corpus", type="default")
print("corpus loaded")


# In[12]:


len(corpus_dict)


# In[13]:


full_corpus_dict = generateCorpus("full_corpus", type="sentence")
print("full_corpus loaded")


# In[14]:


full_corpus_dict['CACM-0270']


# In[15]:


# Load term frequencies
unigrams_dict = generateUnigrams(corpus_dict)
print("Unigrams loaded")
len(unigrams_dict)


# In[19]:


# Compute DF and IDF

df = generateDocumentFrequencies(corpus_dict)
print(len(df))
idf = calculateIDF(corpus_dict, df)
idf['algorithm']


# In[20]:


queries = retrieveQueries("cacm.query.txt")
#queries


# In[21]:


results={}
count = 1
for query in queries:
    query_id = "q_"+str(count)
    print(query_id)
    results[query_id] = sortByScore(queryForResults(query, df, corpus_dict, idf))
    count+=1
    
print("Results generated for all queries")
#results['q_1']


# In[10]:


# Write Results to File

for query_id, query_result in results.items():
    print("Writing result to file "+query_id)
    writeResultsToFile(query_result, "TF_IDF_"+query_id, query_id)


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
print("done")


# In[23]:


query_rel = {}


# In[26]:


query_rel = queryRelevance()
print(len(query_rel.keys()))
print(query_rel["q_1"])


# In[27]:


relevance_set=generateRelevanceSet(query_rel, results)
len(relevance_set)


# In[18]:


# Calculate MRR

mrr_output=calculateMRR(relevance_set)    
mrr_output
mrr_output_string=""
f=open("MRR_TF_IDF.txt", "w+")

for query, mrr_score in mrr_output.items():
    mrr_output_string+=query+" : "+str(mrr_score)+"\n"
f.write(mrr_output_string)
f.close()


# In[65]:


# Calculate P@K

f=open("P@K_TF_IDF.txt", "w+")
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
print("Done")


# In[24]:


# Calculate Mean Average Precision (MAP)

f=open("MAP_TF_IDF.txt", "w+")
mapOutput="MAP SCORES FOR TF IDF \n\n"
    
for query_id in relevance_set.keys():
    mapOutput+=query_id+" : "+str(calculateMAP(relevance_set, query_id))+"\n"
    
f.write(mapOutput)
f.close()
print("Done")


# In[28]:


# Generate all precision tables
for query_id in relevance_set.keys():
    generateAllPrecisionTable(relevance_set, query_id)


# In[30]:


# Generate full Recall tables

for query_id in relevance_set.keys():
    generateRecallTable(relevance_set, query_id)

