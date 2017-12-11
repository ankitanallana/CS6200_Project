To see TF-IDF in action, navigate to the TF_IDF folder and run the TF_IDF_FULL.py file : (enter the following on the command prompt)

python3 TF_IDF_FULL.py

This file generates all query results and snippets for query highlighting. At line 96, you can set an integer for n so that 'n' number of snippets are generated (currently set at 20 - something like 100 takes long to execute for all 64 queries)

-----

To see TF-IDF in action with stopping, navigate to the Stopped Corpus folder and run the TF_IDF_stopped_corpora.py file: (enter the following on the command prompt)

python3 TF_IDF_stopped_corpora.py

This file generates all query results and snippets for query highlighting on the corpus from which stop words were removed. At line 96, you can set an integer for n so that 'n' number of snippets are generated (currently set at 20 - something like 100 takes long to execute for all 64 queries)

-----

To see TF-IDF in action, navigate to the Stemmed corpus folder and run the TF_IDF_stemmed_corpora.py file : (enter the following on the command prompt)

python3 TF_IDF_stemmed_corpora.py

This file generates results on stemmed corpora.

-----

In each respective folder, Query Results and Evaluation (not required for stemmed corpus) have been placed in folders for your review. The Evaluation folder contains three files for P@K, MAP & MRR scores. Two folders with Precision and Recall tables are also present.

-----

Other .py files (apart from the ones mentioned above) are python files which contain helper functions for generating results and evaluation. Text files are the files provided to us (cacm based). The .p files are the pickle files which contain processed corpora & frequencies & IDFs. To generate them again on your computer, you will find a comment just above the lines which read these files(for corpora) - this line can be uncommented and the original line commented so that a fresh pickle file can be generated.

