
# coding: utf-8

# ### All imports

# In[1]:


from tf_idf import *
from evaluation import *


# In[3]:


corpus_dict = loadCorpus("corpus")
print("corpus loaded")


# In[4]:


len(corpus_dict)
corpus_dict['CACM-0637']


# In[5]:


full_corpus_dict = loadCorpus("full_corpus")
print("full_corpus loaded")


# In[6]:


full_corpus_dict['CACM-0270']


# In[7]:


# Load term frequencies
unigrams_dict = generateUnigrams(corpus_dict)
print("Unigrams loaded")
len(unigrams_dict)


# In[8]:


# Compute DF and IDF

df = generateDocumentFrequencies(corpus_dict)
print(len(df))
idf = calculateIDF(corpus_dict, df)
idf['algorithm']


# In[9]:


queries = retrieveQueries("cacm.query.txt")
#queries


# In[10]:


results={}
count = 1
for query in queries:
    query_id = "q_"+str(count)
    print(query_id)
    results[query_id] = sortByScore(queryForResults(query, df, corpus_dict, idf))
    count+=1
    
print("Results generated for all queries")
#results['q_1']


# In[11]:


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


# In[12]:


query_rel = {}


# In[13]:


query_rel = queryRelevance()
print(len(query_rel.keys()))
print(query_rel["q_1"])


# In[14]:


relevance_set=generateRelevanceSet(query_rel, results)
len(relevance_set)


# In[15]:


# Calculate MRR

mrr_output=calculateMRR(relevance_set)    
mrr_output
mrr_output_string=""
f=open("MRR_TF_IDF.txt", "w+")

for query, mrr_score in mrr_output.items():
    mrr_output_string+=query+" : "+str(mrr_score)+"\n"
f.write(mrr_output_string)
f.close()


# In[16]:


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


# In[17]:


# Calculate Mean Average Precision (MAP)

f=open("MAP_TF_IDF.txt", "w+")
mapOutput="MAP SCORES FOR TF IDF \n\n"
    
for query_id in relevance_set.keys():
    mapOutput+=query_id+" : "+str(calculateMAP(relevance_set, query_id))+"\n"
    
f.write(mapOutput)
f.close()
print("Done")


# In[18]:


# Generate all precision tables
for query_id in relevance_set.keys():
    generateAllPrecisionTable(relevance_set, query_id)


# In[19]:


# Generate full Recall tables

for query_id in relevance_set.keys():
    generateRecallTable(relevance_set, query_id)

