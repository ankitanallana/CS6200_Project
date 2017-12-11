import test,make_corpora, time

PATH_TO_CORPUS = "corpus.p"
PATH_TO_STOPWORDS = "common_words.txt"


def make_new_query(a,b):
    resulting_list = list(a)
    temp = []
    with open(PATH_TO_STOPWORDS) as f:
        s = [line.rstrip('\n') for line in f]
    temp.extend(x for x in b if x not in s)
    resulting_list.extend(x for x in temp if x not in resulting_list)
    return resulting_list


def compute_termfreq(list_top_k,file_path):
    return test.main(list_top_k,file_path)


def get_top_k(top_100):
    my_list = []
    with open(top_100 , 'r') as f:
        for line in f:
            my_list.append(line[0:9] + '.html')
    return my_list


def gen_corpus(director,corp):
    return make_corpora.main(director,corp)


def main(query, top_100, top_term):
    """

    :param query: query to be used for the prf
    :param top_100: top 100 documents (names) retrieved with initial query
    :param top_term: The number of terms we want to add to the new query
    :return:
    """

    cleaned_corp = PATH_TO_CORPUS
    list_top_k = get_top_k(top_100)
    new_terms = compute_termfreq(list_top_k,cleaned_corp)
    a = make_new_query(query,new_terms)
    print ("New query:")
    print a[0:top_term-len(query)]
    return a[0:top_term-len(query)]
