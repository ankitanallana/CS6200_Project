# BM25
> "In information retrieval, Okapi BM25 (BM stands for Best Matching) is a ranking function used by search engines to rank matching documents according to their relevance to a given search query. It is based on the probabilistic retrieval framework developed in the 1970s and 1980s by Stephen E. Robertson, Karen Spärck Jones, and others." - Wikipedia
![BM25](https://raw.githubusercontent.com/ankitanallana/CS6200_Project/master/code/BM25/BM25%20Formula.JPG "BM25")

## Variable values

k1 = 1.2
b = 0.75
k2 = 100

## Running the program
Requirements: Python 3 and the associated corpus files in the same folder as the program

### Regular corpus
```python
Python BM25.py
```

### Stemmed corpus
```python
Python BM25.py -stemmed
```

### Stopped corpus
```python
Python BM25.py -stopped
```
