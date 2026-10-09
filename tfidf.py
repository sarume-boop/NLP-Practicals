import math
import re
from collections import Counter


def tokenize(text):
    """
    Convert text into lowercase words.
    """
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())


def calculate_tf(tokens):
    """
    Calculate Term Frequency.

    TF = term_count / total_number_of_terms
    """
    total_words = len(tokens)

    if total_words == 0:
        return {}

    word_count = Counter(tokens)

    tf = {}

    for word, count in word_count.items():
        tf[word] = count / total_words

    return tf


def calculate_idf(documents):
    """
    Calculate Inverse Document Frequency.

    IDF = log(N / DF)

    N  = total number of documents
    DF = number of documents containing the term
    """

    total_documents = len(documents)

    document_frequency = Counter()

    for text in documents.values():

        words = set(tokenize(text))

        for word in words:
            document_frequency[word] += 1

    idf = {}

    for word, df in document_frequency.items():

        idf[word] = math.log(
            total_documents / df
        )

    return idf


def calculate_tfidf(documents):
    """
    Calculate TF-IDF for every document.
    """

    tokenized_documents = {}

    for name, text in documents.items():

        tokenized_documents[name] = tokenize(text)

    idf = calculate_idf(documents)

    tfidf_documents = {}

    for name, tokens in tokenized_documents.items():

        tf = calculate_tf(tokens)

        tfidf = {}

        for word, tf_value in tf.items():

            tfidf[word] = tf_value * idf[word]

        tfidf_documents[name] = tfidf

    return tfidf_documents, idf


def create_vector(tfidf_dict, vocabulary):
    """
    Convert TF-IDF dictionary into numerical vector.
    """

    return [
        tfidf_dict.get(word, 0)
        for word in vocabulary
    ]


def cosine_similarity(vector1, vector2):
    """
    Calculate cosine similarity.
    """

    dot_product = sum(
        a * b
        for a, b in zip(vector1, vector2)
    )

    magnitude1 = math.sqrt(
        sum(a * a for a in vector1)
    )

    magnitude2 = math.sqrt(
        sum(b * b for b in vector2)
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (
        magnitude1 * magnitude2
    )


def search_documents(documents, query):

    tfidf_documents, idf = calculate_tfidf(
        documents
    )

    query_tokens = tokenize(query)

    query_tf = calculate_tf(
        query_tokens
    )

    query_tfidf = {}

    for word, tf_value in query_tf.items():

        if word in idf:

            query_tfidf[word] = (
                tf_value * idf[word]
            )

        else:

            query_tfidf[word] = 0

    vocabulary = sorted(
        set(query_tfidf.keys()).union(
            *[
                set(doc.keys())
                for doc in tfidf_documents.values()
            ]
        )
    )

    query_vector = create_vector(
        query_tfidf,
        vocabulary
    )

    results = []

    for name, tfidf_dict in tfidf_documents.items():

        document_vector = create_vector(
            tfidf_dict,
            vocabulary
        )

        score = cosine_similarity(
            query_vector,
            document_vector
        )

        results.append(
            (name, score)
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results, tfidf_documents