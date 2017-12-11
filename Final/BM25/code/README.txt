BM25
--------

DEFINITION
-----------------
"In information retrieval, Okapi BM25 (BM stands for Best Matching) is a ranking function used by search engines to rank matching documents according to their relevance to a given search query. It is based on the probabilistic retrieval framework developed in the 1970s and 1980s by Stephen E. Robertson, Karen Spärck Jones, and others." - Wikipedia

VARIABLE VALUES
--------------------------
k1 = 1.2 b = 0.75 k2 = 100

RUNNING THE PROGRAM
-----------------------------------
Requirements: Python 3 and the associated corpus files in the same folder as the program

a) Regular corpus: Python BM25.py

b) Stemmed corpus: Python BM25.py -stemmed

c) Stopped corpus: Python BM25.py -stopped

OUTPUT
------------
Output files will be generated in this program folder, BM25_Output folder and Evaluation_Metrics folder

LIBRARIES
---------------
tqdm to display progress of program