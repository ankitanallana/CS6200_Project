Smoothed Query Likelihood Model
--------------------------------------------

DEFINITION
-----------------
"The query likelihood model is a language model used in information retrieval. A language model is constructed for each document in the collection. It is then possible to rank each document by the probability of specific documents given a query. This is interpreted as being the likelihood of a document being relevant given a query." - Wikipedia 

VARIABLE VALUES
--------------------------
lambda = 0.35

RUNNING THE PROGRAM
-----------------------------------
Requirements: Python 3 and the associated corpus files in the same folder as the program

a) Regular corpus: Python QLM.py

b) Stemmed corpus: Python QLM.py -stemmed

c) Stopped corpus: Python QLM.py -stopped

OUTPUT
------------
Output files will be generated in this program folder, QLM_Output folder and Evaluation_Metrics folder

EXTRA
------------
The generateCorpusTF.py script generates a pickle file with the term frequency of all words that occur in the corpus

LIBRARIES
---------------
tqdm to display progress of program