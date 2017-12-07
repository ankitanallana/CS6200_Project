# Evaluation methods - Phase 3

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
        all_precision_values.append(precisionAtK(relevance_set, i, "q_1"))
        
    map_score = sum(all_precision_values)/len(relevance_set[query_id])
    return map_score

# Generates a Precision Table for one query_id
# Writes output to file 
# Function returns output as well - can help in 
# debugging
def generateAllPrecisionTable(relevance_set, query_id):
    f = open("Precision_Table_"+query_id+".txt", "w+")
    
    output = "Precision Table for query - "+query_id+"\n\n"
    
    for k in range(len(relevance_set[query_id])):
        output+=str(i+1)+"\t"+str(precisionAtK(relevance_set, k, "q_1"))+"\n"
    
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
        return 0
    
    else:
        output="Recall Table for "+query_id+"\n\n"
        for i in range(len(relevance_set[query_id])):
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
            
