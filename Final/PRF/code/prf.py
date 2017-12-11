import make_term_frequency_table,make_corpora

PATH_TO_CORPUS = "file/path"
PATH_TO_STOPWORDS = "file/path"
QUERY = 'Automatic Implementation'
TOP_100_DOCUMENTS = 'file/path'
TOP_TERMS = 5
NEW_DIR_LOCATION = "FILE/PATH/newname"

def make_new_query(a,b):
    resulting_list = a.split()
    list_len = len(resulting_list)
    temp = []
    with open(PATH_TO_STOPWORDS) as f:
        s = [line.rstrip('\n') for line in f]
    temp.extend(x for x in b if x not in s)
    resulting_list.extend(x for x in temp if x not in resulting_list)
    return resulting_list,list_len


def compute_termfreq(list_top_k,file_path):
    return make_term_frequency_table.main(list_top_k, file_path)


def get_top_k(top_100):
    my_list = []
    with open(top_100 , 'r') as f:
        for line in f:
            my_list.append(line[0:9] + '.html')
    return my_list


def gen_corpus(director,corp):
    return make_corpora.main(director,corp)


def main(query, top_100, top_term,path_to_new_directory):
    """

    :param query: query to be used for the prf
    :param top_100: top 100 documents (names) retrieved with initial query
    :param top_term: The number of terms we want to add to the new query
    :param path_to_new_directory: dir for storage cleaned corpus
    :return:
    """

    cleaned_corp = gen_corpus(PATH_TO_CORPUS,path_to_new_directory)
    list_top_k = get_top_k(top_100)
    new_terms = compute_termfreq(list_top_k,cleaned_corp)
    new_query,inital_query_length = make_new_query(query,new_terms)
    print ("New query:")
    print new_query[0:top_term+inital_query_length]

main(QUERY,TOP_100_DOCUMENTS,TOP_TERMS,NEW_DIR_LOCATION)
