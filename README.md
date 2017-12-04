# CS6200 Project

#### Documents

| _corpus.p_ | cleaned corpus in a pickle file                                                                                                             |   
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Format:          | ```{'doc_id_1':'doc_content', 'doc_id_2':'doc_content', 'doc_id_3':'doc_content'... }``` |   

| _unigrams.p_ | all unigrams generated from corpus in a pickle file                                                                                                            |   
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Format:          | ```{'unigram_1':{'doc_id_9':frequency of unigram_1 in doc_id_9}, 'unigram_2':{'doc_id_4':frequency of unigram_4 in doc_id_4, 'doc_id_5':frequency of unigram_4 in doc_id_5}}``` |   


_Unigrams_tf_table.txt_ - Term Frequencies of all terms in a **text** file

| _unigrams_tf.p_ | pickle file of all term frequencies                                                                                                             |   
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Format:          | ```{'term_1': frequency of term_1, 'term_2': frequency of term_2}``` |   

^^ Note that these are simply counts of terms over all of the corpus

 
| stopped_corpus.p | corpus with stop words removed                                                                                                             |   
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Format:          | ```{'CACM-0270': ['techniques', 'storage','allocation'...],'CACM-1898': ['regular', 'coulomb', 'wave', 'functions', 'algorithm'] ... }``` |   


 
| stemmed_corpus.p | corpus with stemmed words (provided from cacm_stem.txt)                                                                                                             |   
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Format:          | ```{'CACM-0059': ['survei of progress and trend of develop and us of automat data process in busi and manag control system of the feder govern as of decemb 1957 iii cacm septemb 1959 ca590910 jb '], 'CACM-0060': ['the alpha vector transform of a system of linear constraint cacm septemb 1959 wersan s j ca590909 jb '] ... }``` |   

