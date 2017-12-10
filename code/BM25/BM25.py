import sys
import os
import math
import operator
import pickle
import re
import string
from collections import OrderedDict
from tqdm import *
from evaluation import *

def initialize(indexFile):
    global invertedIndex, queries, corpusDict, corpusSize, k1, b, k2, R, rel;

    #############################
    #######MAGIC NUMBERS#########
    k1 = 1.2;                   #
    b = 0.75;                   #
    k2 = 100;                   #
    #############################

    corpusDict = {};
    corpusSize = 0;
    R = {};
    rel = {};
    invertedIndex = pickle.load( open(indexFile + ".p", "rb"));
    buildR("cacm.rel.txt");   # build R values from camc.rel
    
    if not os.path.exists("BM25_Output"):
        os.makedirs("BM25_Output");

    if not os.path.exists("Evaluation_Metrics"):
        os.makedirs("Evaluation_Metrics");

    ## Build queries array from query file
    queryFile = open("cacm.query.txt", "r");
    queries = [];
    
    q = "";
    if(indexFile == "unigrams_stemmed_corpus"):
        queryFile = open("cacm_stem.query.txt", "r");
        for query in queryFile:
            q += query.replace("\n", "#");
        query = q.split("#");
        query = query[:-1];
        for q in query:
            queries.append(q);
    else:        
        for query in queryFile:
            q += query.replace("<DOC>", "").replace("<DOCNO>", "").replace(" </DOCNO>", ":").replace("</DOC>", "#").replace("\n", " ");
        query = q.split("#");
        query = query[:-1];
        for q in query:
            q = q.split(": ");
            queries.append(q[1]);

## Location string cleaner
def cleanLocation(location):
    location = location.replace('{','').replace('}','').replace(', ','#').replace(' ','').replace("'",'');
    return location;

## Query string cleaner
def cleanQuery(query):
    #regex = "[{}':!,;+-.()]*";
    regex = "[" + string.punctuation + "]*";
    query = query.lower();
    query = re.sub(regex, '', query);
    #query = query.replace('"', '');
    regex = "\t\r\n";
    query = re.sub(regex, " ", query);
    query = query.strip();
    return query

## Content string cleaner
def cleanContent(content):
    content = content.replace(' ','').replace("\n","").replace("'","");
    return content;

## Build dictionary from locations of content
def buildDictionary(location):
    location = location.split('#');
    dictionary = {};
    for l in location:
        i = l.split(":");
        ref = i[0];
        freq = int(i[1]);
        dictionary[ref] = freq;
    return dictionary;

## Split index into Context and Locations
def indexToContextLocations(index):
    index = index.strip();
    index = index.split(": ");
    return index;

## Build the corpus dictionary
def buildCorpusDictionary(dictionary):
    d = {};
    for content in dictionary:
        for doc in dictionary[content]:
            if doc in d:
                d[doc] = d[doc] + dictionary[content][doc];
            else:
                d[doc] = dictionary[content][doc];
    return d;

## Write the output file into the disk in the given format
def writeOutputFile(id, fileName, sysname, dictionary):
    os.makedirs(os.path.dirname(fileName), exist_ok=True);
    with open(fileName, "w") as fileName:
        rank = 1;
        fileName.write("query_id\t\tQ0\tdoc_id\t\trank\t\tBM25_score\t\tsystem_name\n");
        fileName.write("***********************************************************************************************************************************\n");
        for key in dictionary.keys():   # These are sorted per their BM25 scores
            if int(dictionary[key]) < 10 and int(dictionary[key]) > 0:
                score = "0" + str(dictionary[key]);
            else:
                score = str(dictionary[key]);
            fileName.write(str(id) + "\t\tQ0" + "\t" + str(key) + "\t\t" + str(rank) + "\t" + score + "\t" + "BM25_System" + sysname + "\n"); # System name = BM25_System
            rank = rank + 1;
    fileName.close();

## Return the number of occurances of query terms in the corpus dictionary (TF)
def getTermFrequency(queryTerms):
    global corpusDict;
    tf = {};
    for term in queryTerms:
        count = 0;
        term = term.replace(' ','').replace('\n','').replace("'","");
        if term in corpusDict:
            docNos = corpusDict[term]
            for d in docNos:
                count = count + docNos[d];
        tf[term] = count;
    return tf;

## Build TD from query terms
def buildTermDocs(queryTerms):
    global corpusDict;
    td = {};
    for word in queryTerms:
        if word not in corpusDict:
            td[word] = None;
        else:
            countDoc = corpusDict[word];
            docs_term = set();
            for dc in countDoc:
                docs_term.add(dc);
                td[word] = docs_term;
    return td;


## Build document set
def buildDocSet(queryTerms, td):
    documents = set();
    for term in queryTerms:
        docs = td[term];
        if docs != None:
            for d in docs:
                documents.add(d);
    return documents;

## Build R values
def buildR(fileName):
    global R, rel;
    RFile = open(fileName, "r");
    for i in range(1, 65):
        rel[i] = [];
    for line in RFile:
        rel[int(line.split(" ")[0])] += [line.split(" ")[2]];
            
    for d in rel:
        R[d] = len(rel[d]);

## Return BM25 Score for given document d
def generateScores(d, queryTerms, queryID, dictionary2, td):
    global corpusDict, corpusSize, k1, b, k2, R, rel;
    arg = dictionary2[d] / float(corpusSize/float(len(dictionary2))); # divide by total number of keys
    score = 0;
    for term in queryTerms:
        r = 0;
        if term in corpusDict:
            for dd in corpusDict[term]:
                if dd[0] in rel[queryID]:
                    r += 1;
                
        if term not in corpusDict or d not in corpusDict[term]:
            ifd = 0;
        else:
            ifd = corpusDict[term][d];


        K = k1 * ((1 - b) + b * arg);
        if(td[term] != None):
            num1 = (r + 0.5) / (R[queryID] - r + 0.5);
            den1 = (len(td[term]) - r + 0.5) / float(corpusSize - len(td[term]) - R[queryID] + r + 0.5);
            eq1 = (ifd * (k1 + 1)) / (K + ifd);
            eq2 = (queryTerms.count(term) * (k2 + 1)) / (k2 + queryTerms.count(term));
            interim = math.log(num1/den1) * eq1 * eq2;
            score += interim;
    return score;

## Build evaluation metrics
def evaluate(results):
    query_rel = queryRelevance();
    relevance_set=generateRelevanceSet(query_rel, results);

    # Calculate MRR
    mrr_output=calculateMRR(relevance_set);  
    mrr_output;
    mrr_output_string="";
    f=open("Evaluation_Metrics/STOPPED_MRR_TF_IDF.txt", "w+");

    for query, mrr_score in mrr_output.items():
        mrr_output_string+=query+" : "+str(mrr_score)+"\n";
    f.write(mrr_output_string);
    f.close();

    # Calculate P@K
    f=open("Evaluation_Metrics/STOPPED_P@K_TF_IDF.txt", "w+")
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

    # Calculate Mean Average Precision (MAP)

    f=open("Evaluation_Metrics/STOPPED_MAP_TF_IDF.txt", "w+")
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

## Main method to run the program
def main():
    global invertedIndex, queries, corpusDict, corpusSize, k2;
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "-stopped"):
            sysname = "_Stopped";
            initialize("unigrams_stopped_corpus");   # use stopped corpus
        elif(sys.argv[1] == "-stemmed"):    # use stemmed corpus
            sysname = "_Stemmed";
            initialize("unigrams_stemmed_corpus");  # use regular corpus
    else:
        sysname = "_Regular";
        initialize("unigrams");
    for index, locs in invertedIndex.items():
        #index = indexToContextLocations(index);
        content = str(index);
        locations = str(locs);

        # cleanup contant and location
        content = cleanContent(content);
        locations = cleanLocation(locations);

        # build dictionary
        dictionary = buildDictionary(locations);

        # map locations to content
        if content not in corpusDict:
            corpusDict[content] = dictionary

    # Build corpus dictionary and calculate size
    dictionary2 = buildCorpusDictionary(corpusDict);
    for key in dictionary2:
            corpusSize += dictionary2[key];

    # Process for each query
    results = {};
    queryID = 0
    for query in tqdm(queries):
        queryID = queryID + 1;
        query = cleanQuery(query);  # clean the query
        queryTerms = query.split(" ");  # split query into query terms
        td = buildTermDocs(queryTerms);  # generate td
        tf = getTermFrequency(queryTerms); # generate tf   
        documents = buildDocSet(queryTerms, td);    # build documinent set
        # Generate BM25 Scores
        BM25Scores = {};
        docScorePairs = [];
        for d in documents:
            BM25Scores[d] = generateScores(d, queryTerms, queryID, dictionary2, td);
            docScorePairs += [(d, BM25Scores[d])];
            
        docScorePairs = sorted(docScorePairs, key=operator.itemgetter(1), reverse=True);
        results['q_' + str(queryID)] = docScorePairs;
        
        # Sort dictionary by their BM25 scores
        sortedDict = OrderedDict(sorted(BM25Scores.items(), key=operator.itemgetter(1), reverse=True)[:k2]);

        # Write file to disk with given file name
        fileName = "BM25_Output/Query_" + str(queryID) + ".txt";
        writeOutputFile(queryID, fileName, sysname, sortedDict);
    evaluate(results);   # Evaluate scores generated

main(); # run the program
