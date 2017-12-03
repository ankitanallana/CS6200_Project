# CS6200 Project

#### Documents

_corpus.p_ - cleaned corpus in a pickle file

Format: `{'doc_id_1':'doc_content', 'doc_id_2':'doc_content', 'doc_id_3':'doc_content'...}`

_unigrams.p_ - all unigrams generated from corpus in a pickle file

Format : 

```{'unigram_1':{'doc_id_9':frequency of unigram_1 in doc_id_9}, 'unigram_2':{'doc_id_4':frequency of unigram_4 in doc_id_4, 'doc_id_5':frequency of unigram_4 in doc_id_5}}```

_Unigrams_tf_table.txt_ - Term Frequencies of all terms in a text file

_unigrams_tf.p_ - pickle file of all term frequencies

Format:

```{'term_1': frequency of term_1, 'term_2': frequency of term_2}```

Note that these are simply counts of terms over all of the corpus