
# coding: utf-8

# ### Imports

# In[1]:


import os
import nltk
import pickle
import re
from nltk.tokenize import word_tokenize
import string
import collections
import math
import operator


# #### Helper functions for cleaning corpus

# In[2]:


regex = "["+string.punctuation+"]*"
timestamp_regex1 = "[A-Za-z]+\s[0-9]+,\s[0-9]+\s+[0-9]+:[0-9]+\s[AM]*[PM]*"
timestamp_regex2 ="[A-Za-z]+,\s[0-9]+"
# Remove Punctuation
def remove_punctuation(text):
    text = re.sub(regex, '', text)
    return text


# Clean the document content
def clean_content(text):
    
    # Remove html code
    # Rvery document in this corpus contains only two kinds
    # of HTML tags
    
    text = re.sub('<html>', '', text)
    text = re.sub('<pre>', '', text)
    text = re.sub('</html>', '', text)
    text = re.sub('</pre>', '', text)
    
    # Remove timestamp
    text = re.sub(timestamp_regex1, '', text)
    
    # Remove timestamp
    text = re.sub(timestamp_regex2, '', text)
    
    # Remove punctuation
    text = remove_punctuation(text)
    
    # Remove numbers towards the end of the file
    text = re.sub('[0-9]+\s[0-9]+\s[0-9]+','', text)
    
    # Split into tokens
    tokens = word_tokenize(text.lower())
    
    return tokens


# ### Load the corpus

# In[4]:


# cwd = os.getcwd()+"/cacm/"
# list_dir = os.listdir(cwd)

# corpus_dict = {}

# print("Processing all files")

# for l in list_dir:
#     f = open(cwd+l, "r+")
#     doc_id = l.split(".html")
#     doc_content=clean_content(f.read())
#     corpus_dict[doc_id[0]]=doc_content
    
# print("Writing to pickle file")
# pickle.dump(corpus_dict, open(os.getcwd()+"/corpus.p", "wb"))

corpus_dict = dict(pickle.load(open(os.getcwd()+"/corpus.p", "rb"), encoding="utf-8"))
print("corpus loaded")


# ### Generate Document Frequencies (DF)

# In[5]:


# print("Constructing inverse map for unigrams for files ")
# unigram_dict_inverse={}
# unigram_dict={}
# for c, words in corpus_dict.items():
#     unigram_dict_inverse[c] = dict(collections.Counter(words))
# print("Inverse map constructed") 

# print("Constructing unigrams index")
# for c, words in unigram_dict_inverse.items():
#     for word, freq in words.items():
#         if word not in unigram_dict:
#             unigram_dict[word] = {}
#         temp_dict = unigram_dict[word]
#         temp_dict[c] = freq
#         unigram_dict[word]=temp_dict
    
# print("Unigrams inverted index constructed!")
# pickle.dump(unigram_dict, open("unigrams.p","wb"))


# Write Unigrams Inverted Index to file
# print("Writing Unigrams inverted index to file")
# f = open("Unigrams.txt","w+")
# for k, v in unigram_dict.items():
#     f.write(k+" : "+str(v)+"\n")
# f.close()



# In[ ]:


# Load unigrams df

unigram_dict=dict(pickle.load(open(os.getcwd()+"/unigrams.p", "rb"), encoding="utf-8"))
print("Unigrams loaded")


# In[6]:


# Generate Term Frequencies (IDF)

# unigram_freq_table={}
# print("Constructing an inverted index from unigrams")
# f=open("Unigrams_tf_table.txt","w+")

# # Constructing the term frequency table
# for k, values in unigram_dict.items():
#     unigram_freq_table[k]=sum(values.values())
    
# print("Frequencies calculated")
# for k, v in unigram_freq_table.items():
#     f.write(str((k, v))+"\n")
    
# f.close()


# pickle.dump(unigram_dict, open("unigrams_tf.p","wb"))


# In[ ]:


# Load Term Frequencies
unigram_freq_table=dict(pickle.load(open(os.getcwd()+"/unigrams_tf.p", "rb"), encoding="utf-8"))
print("Term Frequencies loaded")


# In[12]:


# Calculate IDF
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it)

idf={}
N = len(corpus_dict)
for term in unigram_dict.keys():
    idf[term] = math.log(N/len(unigram_freq_table[term].keys()))
    
print("IDF calculated!")
#TODO : Write to PICKLE FILE and load


# In[13]:


# Calculate TF-IDF for every document per query
# Sample query - Automatic Implementation

query = "Automatic Implementation"
ranked_documents = {}
unigram_dict['automatic']
doc_list = []
for terms in word_tokenize(query.lower()):
    
    # Retrieve inverted list for term
    for k in unigram_dict[terms].keys():
        if k not in doc_list:
            doc_list.append(k)
        

for d in doc_list:
    doc_len = len(corpus_dict[d])
    score = 0.0
    for term in word_tokenize(query.lower()):
        if d in unigram_dict[term].keys():
            tf_term = unigram_dict[term][d]/doc_len
            idf_term = idf[term]
            score+= tf_term * idf_term
        
    ranked_documents[d]=score


# In[14]:


len(ranked_documents)

# sort by rank 
rank_sort = sorted(ranked_documents.items(), key=operator.itemgetter(1), reverse=True)

output=""
f = open("q_test.txt","w+")
for i in range(100):
    doc, score = rank_sort[i]
    output+=str(doc)+" : "+str(score)+"\n"
f.write(output)
f.close()
#output


# ### Task 3 
# 
# #### Removing stop words from the corpus

# In[16]:


stop_words = [word.rstrip('\n') for word in open('common_words')]
#stop_words


# In[20]:


diff = lambda l1,l2: [x for x in l1 if x not in l2]


# In[107]:


stopped_corpus = {}

for doc, content in corpus_dict.items():
    stopped_corpus[doc] = diff(content, stop_words)

print(len(stopped_corpus))

#stopped_corpus


# In[109]:


pickle.dump(stopped_corpus, open("stopped_corpus.p","wb"))
print("Stopped corpus written to file")

#TODO - load stopped corpus the next time


# #### Using stemmed corpus

# In[100]:


# Reading and parsing the stemmed corpus
# provided in cacm_stem.txt
stemmed_corpus_temp = {}
with open('cacm_stem.txt') as f:
    content = f.readlines()
#print(content)
pattern = '#\s[0-9]+'
for item in content:
    if re.match(pattern, item) :
        doc_id = re.split('#\s', item.strip())
        doc_id = doc_id[1]
        #print(doc_id)
        stemmed_corpus_temp[doc_id]=[]
    else:
        stemmed_corpus_temp[doc_id].append(item.strip())
stemmed_corpus_temp


# In[108]:


# Process the content in every document
# i.e. remove those strings which contain ONLY numbers and timestamps

# Should we index terms like 'ca581001' ?

stemmed_corpus={}
for doc_id, content in stemmed_corpus_temp.items():
    new_doc_id = "CACM-"+str(doc_id).zfill(4)
    stemmed_corpus[new_doc_id]=[]
    temp_list = []
    #print(str(doc_id).zfill(4))
    flag = 0
    for line in content:
        if re.match('^ *[0-9][0-9 ]*$', line)==None:
            temp_list.append(line)
    
    all_content = " ".join(temp_list)
    split_content = all_content.split('[a-z]+\s[0-9]+\s[0-9]+\s[0-9]+\s[0-9]+\s[am|pm]+')[0]
    final_content=re.sub('[a-z]+\s[0-9]+\s[0-9]+\s[0-9]+\s[0-9]+\s[am|pm]+[\s0-9]*','', split_content)
    #print(final_content)
    stemmed_corpus[new_doc_id].append(final_content)
    
print(len(stemmed_corpus))

stemmed_corpus


# In[103]:


pickle.dump(stemmed_corpus, open("stemmed_corpus.p","wb"))
print("Done")

#TODO - load stemmed corpus the next time

