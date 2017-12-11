
# coding: utf-8

# ### Imports

# In[1]:


import os
import nltk
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import string
import collections
import math
import operator


# ### Helper functions for cleaning corpus

# In[2]:


regex = "["+string.punctuation+"]*"
regex = re.sub('-','', regex)
timestamp_regex1 = "[CA]+[0-9]+\s[JB]+\s[A-Za-z]+\s[0-9]+,\s[0-9]+\s+[0-9]+:[0-9]+\s[AM]*[PM]*"
timestamp_regex2 ="[CACM]+\s[A-Za-z]+,\s[0-9]+"

# Get the last index of a value from a list
def getLastIndexOf(a_list, a_value):
    return len(a_list) - a_list[::-1].index(a_value) - 1


# Remove Punctuation
def remove_punctuation(text):
    text = re.sub(regex, '', text)
    text = re.sub('-', ' ', text)
    return text


# Clean the document content
def clean_content(text):
    
    # Remove html code
    # Every document in this corpus contains only two kinds
    # of HTML tags
    
    text = re.sub('<html>', '', text)
    text = re.sub('<pre>', '', text)
    text = re.sub('</html>', '', text)
    text = re.sub('</pre>', '', text)
    
    # Remove timestamp
    #text = re.sub(timestamp_regex1, '', text)
    #print(text)
    
    # Remove timestamp
    #text = re.sub(timestamp_regex2, '', text)
    #print(text)
    
    # Remove punctuation
    text = remove_punctuation(text)
    #print(text)

    # Remove full stops at the end of sentences
    # preserve them in other cases
    #text = re.sub("\. ", ' ', text)
    #print(text)

    # Remove numbers towards the end of the file
    text = re.sub('[0-9]+\s[0-9]+\s[0-9]+','', text)
    #print(text)

    # Split into tokens
    tokens = word_tokenize(text.lower())
    
    return tokens

def retrieve_sentences(text):
    
    # Remove html code
    # Every document in this corpus contains only two kinds
    # of HTML tags
    
    text = re.sub('<html>', '', text)
    text = re.sub('<pre>', '', text)
    text = re.sub('</html>', '', text)
    text = re.sub('</pre>', '', text)
    
    # Remove timestamp
    #text = re.sub(timestamp_regex1, '', text)
    
    # Remove timestamp
    #text = re.sub(timestamp_regex2, '', text)
    
    # Remove numbers towards the end of the file
    text = re.sub('[0-9]+\s[0-9]+\s[0-9]+','', text)
    
    # Remove tabs
    text = re.sub('\t', ' ', text)
    
    # Remove extra \n or \t
    text = text.strip()
    
    # Split into sentences 
    temp_sentences = re.split('\n\n+', text)
    
    # Replace \n
    # temp_sentences = [re.sub('\n[A-Z]', '. ', s) for s in temp_sentences]
    # temp_sentences = [re.sub('\n[a-z]', ' ', s) for s in temp_sentences]
    
    temp_sentences = [re.sub('\n', ' ', s) for s in temp_sentences]
    
    sentences = []
    
    for s in temp_sentences:
        temp_s = s.split(". ")
        for t_s in temp_s:
            sentences.append(t_s.strip())
    
    return sentences


# ### Load the corpus

# In[3]:


def generateCorpus(pickle_file_name, type="default"):
    cwd = os.getcwd()+"/cacm/"
    list_dir = os.listdir(cwd)

    full_corpus_dict = {}

    print("Processing all files")

    for l in list_dir:
        f = open(cwd+l, "r+")
        doc_id = l.split(".html")
        if "default" in type:
            doc_content = clean_content(f.read())
        else:
            doc_content = retrieve_sentences(f.read())
        full_corpus_dict[doc_id[0]] = doc_content
        

    pickle.dump(full_corpus_dict, open(os.getcwd()+"/"+pickle_file_name+".p", "wb"))
    print("corpus written to pickle file")
    return full_corpus_dict

def loadCorpus(pickle_file_name):
    return dict(pickle.load(open(os.getcwd()+"/"+pickle_file_name+".p", "rb"), encoding="utf-8"))


# ### Generate Document Frequencies (DF)

# In[4]:


# Calculate IDF
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it)

def calculateIDF(corpus_dict, unigram_dict):

    idf={}
    N = len(corpus_dict)
    for term in unigram_dict.keys():
        idf[term] = math.log(N/len(unigram_dict[term].keys()))

    print("IDFs calculated!")

    pickle.dump(idf, open("idf.p", "wb"))
    print("IDFs written to file idf.p")
    return idf


# In[5]:


# Calculate TF-IDF for every document per query
def queryForResults(query, unigram_dict, corpus_dict, idf):

    ranked_documents = {}
    #unigram_dict['automatic']
    doc_list = []
    for term in word_tokenize(query.lower()):
        
        # Retrieve inverted list for term
        if term in unigram_dict.keys():
            for k in unigram_dict[term].keys():
                if k not in doc_list:
                    doc_list.append(k)


    for d in doc_list:
        doc_len = len(corpus_dict[d])
        score = 0.0
        
        for term in word_tokenize(query.lower()):
            if term in unigram_dict.keys():
                if d in unigram_dict[term].keys():
                    tf_term = unigram_dict[term][d]/float(doc_len)
                    idf_term = idf[term]
                    score+= tf_term * idf_term
        ranked_documents[d]=score

    return ranked_documents
        
def sortByScore(result_set):
    return sorted(result_set.items(), key=operator.itemgetter(1), reverse=True)


# In[6]:


def writeResultsToFile(rank_sort, file_name, query_id):
    output=""
    f = open(file_name+".txt","w+")
    stop_index = 100
    if len(rank_sort)<100:
        stop_index = len(rank_sort)
    for i in range(stop_index):
        doc, score = rank_sort[i]
        output+=query_id+" "+"Q0 "+ doc + " " + str(i+1) + " " + str(score) + " TF_IDF " + "\n"
        #output+=str(doc)+" : "+str(score)+"\n"
    f.write(output)
    f.close()
    print("done")


# ### Task 3 
# 
# #### Removing stop words from the corpus

# In[7]:


# Lambda function to produce difference of two LISTS
diff = lambda l1,l2: [x for x in l1 if x not in l2]


# In[8]:


# Generate corpus - remove all stopwords
def generateStoppedCorpus(corpus_dict, stop_words):

    stopped_corpus = {}

    for doc, content in corpus_dict.items():
        temp_list = diff(content, stop_words)
        stopped_corpus[doc] = " ".join(temp_list)
        pickle.dump(stopped_corpus, open("stopped_corpus.p","wb"))
    print("Stopped corpus written to file")
    return stopped_corpus



# ### Using stemmed corpus

# In[9]:


# Reading and parsing the stemmed corpus
# provided in cacm_stem.txt
# A separate function was required because loading this corpus required
# a different set of steps for file processing

def loadStemmedCorpus(file_name):

    stemmed_corpus_temp = {}
    with open(file_name) as f:
        content = f.readlines()
    pattern = '#\s[0-9]+'
    for item in content:
        if re.match(pattern, item) :
            doc_id = re.split('#\s', item.strip())
            doc_id = doc_id[1]
            stemmed_corpus_temp[doc_id]=[]
        else:
            stemmed_corpus_temp[doc_id].append(item.strip())
            
    stemmed_corpus={}

    for doc_id, content in stemmed_corpus_temp.items():
        new_doc_id = "CACM-"+str(doc_id).zfill(4)
        stemmed_corpus[new_doc_id]=[]
        temp_list = []
        flag = 0
        for line in content:
            if re.match('^ *[0-9][0-9 ]*$', line)==None:
                temp_list.append(line)

        all_content = " ".join(temp_list)
        
        #Isolate and remove timestamps
        split_content = all_content.split('[a-z]+\s[0-9]+\s[0-9]+\s[0-9]+\s[0-9]+\s[am|pm]+')[0]
        final_content=re.sub('[a-z]+\s[0-9]+\s[0-9]+\s[0-9]+\s[0-9]+\s[am|pm]+[\s0-9]*','', split_content)
        stemmed_corpus[new_doc_id].append(final_content)
        
        pickle.dump(stemmed_corpus, open("stemmed_corpus.p","wb"))
    
    print("Stemmed corpus written to file")

            
    return stemmed_corpus



# ### Snippet Generation

# In[10]:


def generateSnippets(rank_sort_temp, full_corpus_dict, query, n):

    snippets = {}
    rank_sort_temp = rank_sort_temp[:n]
    for entry in rank_sort_temp:
        document, score = entry
        snippets[document] = []
        count=0
        sentence_list={}

        for s in full_corpus_dict[document]:
            first_index = 5
            end_index = 0
            temp=[]
            s = s.lower()
            for term in word_tokenize(query.lower()):
                temp = word_tokenize(s)
                temp_lower = word_tokenize(s.lower())
                flag = False
                if term in temp_lower :
                    flag = True
                    if temp_lower.index(term) < first_index :
                        first_index = temp_lower.index(term)
                    if getLastIndexOf(temp_lower, term) >= end_index:
                        end_index = getLastIndexOf(temp_lower, term)

                if flag == True:

                    if first_index < 5 : 
                        first_index = 0
                    else:
                        first_index -= 5
                    if (len(temp_lower)-end_index) < 5:
                        end_index = len(temp_lower)
                    else:
                        end_index +=  5
                    formatted_string = "..."+" ".join(temp[first_index:end_index+1])+"..."
                    if formatted_string not in snippets[document]:
                        if count not in sentence_list:
                            sentence_list[count]=[]
                        sentence_list[count].append(formatted_string)
                            
        count+=1
        
        # Extract the longest sentence
        temp_sentence_list = []
        max_length=0
        max_index = 0
        for index, sentences in sentence_list.items():
            for i in range(len(sentences)):
                if len(sentences[i]) > max_length:
                    max_length = len(sentences[i])
                    max_index = i
            temp_sentence_list.append(sentence_list[index][max_index])
        snippets[document] = temp_sentence_list        
    return snippets 

# In[11]:


# Generate HTML files for Query Highlighting

def generateHTML(snippets, rank_sort_temp, query, n):
    
    rank_sort_temp = rank_sort_temp[:n]

    html_file_begin="<html><body><h2>Top 20 Retrieval results : TF-IDF </h2>"
    html_file_begin+="<h3> Query : "+query+"</h3>"
    html_file_begin+="<p>"

    query = remove_punctuation(query.lower())
    
    for i in range(len(rank_sort_temp)):
        doc, score = rank_sort_temp[i]
        sn = snippets[doc]
        html_file_begin+="<h4>"+doc+"</h4>"
        for s in sn:
            for term in word_tokenize(query):
                if term in s:
                    s = re.sub(term+"[\s]+", "<b> "+term+" </b>", s, re.IGNORECASE)
                
            html_file_begin+=s+"<br>"
        html_file_begin+="</p><p>"
    html_file_begin+="</p>"

    
    html_file_begin+="</body></html>"
    return html_file_begin



# ### Generate results per query using TF-IDF Model

# In[12]:


def retrieveQueries(file_path):
    queryFile = open(file_path, "r");
    queries = [];
    
    q = "";
    for query in queryFile:
        q += query.replace("<DOC>", "").replace("<DOCNO>", "").replace(" </DOCNO>", ":").replace("</DOC>", "#").replace("\n", " ").replace("\t", " ");
    query = q.split("#");
    query = query[:-1];
    for q in query:
        q = q.split(": ");
        queries.append(q[1].strip());
    return queries

## Calculate Term Frequencies across documents

def generateUnigrams(corpus_dict):
    unigrams_dict={}
    for c, words in corpus_dict.items():
        temp_dict = dict(collections.Counter(words))
        for k, v in temp_dict.items():
            if k not in unigrams_dict:
                unigrams_dict[k]=1
                
            else:
                temp_count = unigrams_dict[k]
                temp_count += 1
                unigrams_dict[k] = temp_count
    
    pickle.dump(unigrams_dict, open(os.getcwd()+"/unigrams_tf"+".p", "wb"))
    print("term frequencies across the corpus written to pickle file")
    return unigrams_dict

## Calculate document frequencies across documents

def generateDocumentFrequencies(corpus_dict):
    df={}
    for doc, words in corpus_dict.items():
        for word in words:
            if word not in df:
                temp_dict = {}
                temp_dict[doc]=1
                df[word]=temp_dict
            else:    
                temp_dict = df[word]
                if doc in temp_dict.keys():
                    temp_count = temp_dict[doc]
                    temp_count+=1
                    temp_dict[doc] = temp_count
                    
                else:
                    temp_dict[doc]=1
                df[word] = temp_dict
    pickle.dump(df, open(os.getcwd()+"/df"+".p", "wb"))
    print("documents frequencies across the corpus written to pickle file")    
    return df
