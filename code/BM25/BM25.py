import sys
import os
import math
import operator
import pickle
from collections import OrderedDict
from tqdm import *


def initialize(indexFile):
    global invertedIndex, queries, corpusDict, corpusSize, k1, b, k2;

    #############################
    #######MAGIC NUMBERS#########
    k1 = 1.2;                   #
    b = 0.75;                   #
    k2 = 100;                   #
    #############################

    corpusDict = {};
    corpusSize = 0;
    #invertedIndex = pickle.load( open("unigrams.p", "rb"));
    invertedIndex = pickle.load( open(indexFile + ".p", "rb"));
    
    if not os.path.exists("BM25_Output"):
        os.makedirs("BM25_Output");

    ## Build queries array from query file

    queryFile = open("cacm.query.txt", "r");
    queries = [];
    
    q = "";
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
    query = query.lower().replace('{','').replace('}','').replace("[","").replace("]","").replace(',','').replace("'",'').replace("-", " ").replace(":","").replace("!","").replace("\t", " ").replace("\r"," ").replace("\n"," ").replace("(", "").replace(";", "").replace(")","").strip();
    return query;

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
def writeOutputFile(id, fileName, dictionary):
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
            fileName.write(str(id) + "\t\tQ0" + "\t" + str(key) + "\t\t" + str(rank) + "\t" + score + "\t" + "BM25_System\n"); # System name = BM25_System
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

## Return BM25 Score for given document d
def generateScores(d, queryTerms, dictionary2, td):
    global corpusDict, corpusSize, k1, b, k2;
    arg = dictionary2[d] / float(corpusSize/float(len(dictionary2))); # divide by total number of keys
    score = 0;
    for term in queryTerms:
        if term not in corpusDict or d not in corpusDict[term]:
            ifd = 0;
        else:
            ifd = corpusDict[term][d];
        eq1 = ifd * (k1+1);	  
        eq2 = queryTerms.count(term) * (k2 + 1);
        if td[term] == None:
            eq3 = len(dictionary2);
            thirdDenominator = (0.5 / float (eq3 + 0.5));
        else:
            eq3 = (len(dictionary2) - len(td[term]));
            thirdDenominator = ((len(td[term]) + 0.5) / float (eq3 + 0.5));
        first = (eq1 /((b * arg) + (k1 * (1-b)) + ifd));
        second = (eq2 / (k2 + queryTerms.count(term)));
        thirdNumerator = 1;
        
        if (not (thirdNumerator < 0 and thirdDenominator > 0) or (thirdNumerator > 0 and thirdDenominator < 0)):
            interim = math.log(thirdNumerator/thirdDenominator) * first * second;
            score = score + interim;
    return score;

## Main method to run the program
def main():
    global invertedIndex, queries, corpusDict, corpusSize, k2;
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "-stopped"):
            initialize("unigrams_stopped_corpus");   # use stopped corpus
        elif(sys.argv[1] == "-stemmed"):    # use stemmed corpus
            initialize("unigrams_stemmed_corpus");  # use regular corpus
    else:
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
    queryID = 0
    for query in tqdm(queries):
        queryID = queryID + 1;
        query = cleanQuery(query);  # clean the query
        queryTerms = query.split(" ");  # split query into query terms
        td = buildTermDocs(queryTerms);  # generate td
        tf = getTermFrequency(queryTerms); # generate tf   
        documents = buildDocSet(queryTerms, td);    # build document set
        # Generate BM25 Scores
        BM25Scores = {};
        for d in documents:
            BM25Scores[d] = generateScores(d, queryTerms, dictionary2, td);

        # Sort dictionary by their BM25 scores
        sortedDict = OrderedDict(sorted(BM25Scores.items(), key=operator.itemgetter(1), reverse=True)[:k2]);

        # Write file to disk with given file name
        fileName = "BM25_Output/Query_" + str(queryID) + ".txt";
        writeOutputFile(queryID, fileName, sortedDict);
        

main(); # run the program
