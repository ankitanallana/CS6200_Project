# Evaluation methods - Phase 3

# relevance_set can be generated by :
# generateRelevanceSet(query_rel, results)

# query_rel can be generated by :
# query_rel = queryRelevance()

# results can be generated by :
# results = generateResults(queries)

# queries can be generated by :
# queries = retrieveQueries("cacm.query.txt") from tf_idf.py

# ALL IMPORTS

from tf_idf import *

# Calculate MRR
# Returns MRR for a dict of queries
def calculateMRR(relevance_set):

    mrr = {}
    for query_id, rel_set in relevance_set.items():

        if 'R' in rel_set:
            rank = rel_set.index('R')
            rank+=1 						#  because list indices start from 0
            mrr[query_id]=1/float(rank)
        else:
            mrr[query_id] = 'N/A' 			#  No relevant document retrieved so far
    return mrr

# Calculate P@K
# Returns Precision at 'K' rank for one query_id
def precisionAtK(relevance_set, K, query_id):
    count=1
    rel_set=relevance_set[query_id]
    #print(rel_set)
    
    subset = rel_set[:K]
    dict_items = dict(collections.Counter(subset))
    #print(dict_items.keys())
    
    if 'R' not in dict_items.keys():
        return 0.0
    else:
        return dict_items['R']/K

# Calculate Mean Average Precision (MAP)
# Returns Mean Average Precision for one query_id
def calculateMAP(relevance_set, query_id):
    all_precision_values=[]
    
    for i in range(len(relevance_set[query_id])):
        all_precision_values.append(precisionAtK(relevance_set, i, query_id))
        
    map_score = sum(all_precision_values)/len(relevance_set[query_id])
    return map_score

# Generates a Precision Table for one query_id
# Writes output to file 
# Function returns output as well - can help in 
# debugging
def generateAllPrecisionTable(relevance_set, query_id):
    f = open("Precision_Table_"+query_id+".txt", "w+")
    
    output = "Precision Table for query - "+query_id+"\n\n"
    stop_index = 100
    if len(relevance_set[query_id])<100:
        stop_index=len(relevance_set[query_id])
    for k in range(stop_index):
        output+=str(k+1)+"\t"+str(precisionAtK(relevance_set, k, "q_1"))+"\n"
    
    f.write(output)
    f.close()
    print("Precision Table written to ", "PrecisionTable_"+query_id+".txt")
    return output

# Generate Recall table for one query_id
# Writes output to file
# Also returns output - can help in debugging
def generateRecallTable(relevance_set, query_id):
    
    f = open("Recall_Table_"+query_id+".txt", "w+")
    
    rel_set = relevance_set[query_id]
    dict_items = dict(collections.Counter(rel_set))
    
    if 'R' not in dict_items.keys():
        print("No relevant documents retrieved so far")
        f.write("No relevant documents retrieved so far")
        f.close()
        return 0
    
    else:
        stop_index = 100
        if len(relevance_set[query_id])<100:
            stop_index=len(relevance_set[query_id])
    
        output="Recall Table for "+query_id+"\n\n"
        for i in range(stop_index):
            output+=str(i+1)+"\t"+str(recallAtK(rel_set, i, dict_items['R']))+"\n"
        
        print(output)
        
        f.write(output)
        f.close()
    
        return output

# Computes Recall at rank K
def recallAtK(rel_set, i, num_rel):
    subset=rel_set[:i]
    dict_items = dict(collections.Counter(subset))
    
    if 'R' in dict_items.keys():
        num=dict_items['R']
        return float(num)/num_rel
    else:
        return 0.0
 
# Generates a dict per query marking documents as
# relevant or not
# Output : {q_1:[R, R, R, N, R], q_2:[N, R, N, N, R]}
def generateRelevanceSet(query_rel, results):
    relevance_set = {}

    for query_id in query_rel.keys():
        docs = results[query_id]
        relevance_set[query_id] = []
        for d in docs:

            doc, score = d
            if doc in query_rel[query_id]:
                relevance_set[query_id].append('R')
            else:
                relevance_set[query_id].append('N')
    return relevance_set           

# Read the relevance judgements provided
# and stores in a dict
# Output : {q_1:['CACM-0008.html', 'CACM-0098.html'], q_2:['CACM-0008.html', 'CACM-0098.html']}
def queryRelevance():
    query_rel={}
    with open("cacm.rel.txt") as f:
        content = f.readlines()

    count = 1
    for line in content:
        contents = line.split(" ")
        query_id = "q_"+str(contents[0])
        if query_id not in query_rel.keys():
            query_rel[query_id]=[]
        query_rel[query_id].append(contents[2])
    
    return query_rel

# Generates results per query and stores it in a dict
# Currently just TF-IDL - branching statements can be
# added to call BM25 and QLM models
# Also returns a "query_map" 
# query_map : {'q_1': 'what articles exist which deal with tss time sharing system an operating system for ibm computers',
# 'q_10': 'parallel languages languages for parallel computation',
# 'q_11': 'setl very high level languages'... }    
# results : {'q_1':[...list of 100 docs], 'q_2':[...list of 100 docs]}
def generateResults(queries, df, corpus_dict, idf):

    results = {}
    count = 1
    query_map = {}
    
    for query in queries:
        # Process queries the way the corpus was
        query = query.lower()
        query = remove_punctuation(query)
        query_id = "q_"+str(count)
        results[query_id] = sortByScore(queryForResults(query, df, corpus_dict, idf))[:100]
        query_map[query_id] = query
        count = count+1
    return results, query_map