# Smoothed QLM
> "The query likelihood model is a language model used in information retrieval. A language model is constructed for each document in the collection. It is then possible to rank each document by the probability of specific documents given a query. This is interpreted as being the likelihood of a document being relevant given a query." - Wikipedia
![QLM](https://raw.githubusercontent.com/ankitanallana/CS6200_Project/master/code/Smoothed_QLM/QLM%20Formula.JPG "QLM")

## Variable values

lambda = 0.35

## Running the program
Requirements: Python 3 and the associated corpus files in the same folder as the program

### Regular corpus
```python
Python QLM.py
```

### Stemmed corpus
```python
Python QLM.py -stemmed
```

### Stopped corpus
```python
Python QLM.py -stopped
```

## Output
Output files can be found in the root/data/QLM_Output folder
