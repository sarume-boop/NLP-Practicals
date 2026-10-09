TF-IDF DOCUMENT SEARCH ENGINE
=============================

Topic:
TF-IDF Based Document Search and Relevance Ranking System

Technology:
Python
Tkinter

Concepts Demonstrated:
1. Term Frequency (TF)
2. Inverse Document Frequency (IDF)
3. TF-IDF
4. Vector Space Model
5. Cosine Similarity
6. Relevance Ranking
7. Information Retrieval

PROJECT STRUCTURE
-----------------

tfidf_assignment/
│
├── main.py
├── tfidf.py
├── documents.py
└── README.txt


HOW TO RUN
-----------

Step 1:
Open the project folder in VS Code.

Step 2:
Open the terminal.

Step 3:
Run:

python main.py


No third-party package is required.


HOW THE SYSTEM WORKS
--------------------

User enters search query
        ↓
Tokenization
        ↓
Calculate TF
        ↓
Calculate IDF
        ↓
Calculate TF-IDF
        ↓
Create document vectors
        ↓
Create query vector
        ↓
Calculate cosine similarity
        ↓
Rank documents
        ↓
Display results in UI