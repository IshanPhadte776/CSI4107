# The Code Shouldn't take more than 5 Seconds to Run

# regular expression (regex) module in Python. Patterns used to match character combinations in strings.
import re
# Natural Language Toolkit (NLTK)
import nltk

import math
import os
# Stopwords are like basic non-special words
from nltk.corpus import stopwords
# Imported just incase someone wanted to use it
from nltk.stem import PorterStemmer
# For parsing
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

from lxml import etree

# For Dictionaries
from collections import defaultdict

# Part 1
print("Part 1 running...")


def preprocess(text):
    # Remove markup that is not part of the text
    text = re.sub(r'<.*?>', '', text)

    # Tokenization - Split the text into words
    tokens = re.findall(r'\b\w+\b', text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Don't use Porter Stemmer, it cuts some words off incorrectly, (Cut officers to offic)
    # Using Porter does feel to speed up the code
    # porter = PorterStemmer()
    # tokens = [porter.stem(word) for word in tokens]

    return tokens


# Part 2
print("Part 2 running...")
# Creates the inverted index for 1 document


def buildInvertedIndex(doc_id, tokens):
    inverted_index = {}

    # For every token(word)
    for position, token in enumerate(tokens):
        # Add the token to inverted index / position
        if token not in inverted_index:
            inverted_index[token] = [(doc_id, position)]
        else:
            inverted_index[token].append((doc_id, position))

    return inverted_index


# Get the root

# If multiple parents, wrap in another tag as root


# Part 3 Goes Here
print("Part 3 running...")


def idf(term, N, frequency):
    return math.log((N - frequency[term] + 0.5) / (frequency[term] + 0.5) + 1)


def bm25(doc, query, N, doc_freq, avgdl):
    k1 = 1.5
    b = 0.75
    score = 0
    length = len(doc)
    for word in query:
        if word in doc:
            f = doc.count(word)
            idf_score = idf(word, N, doc_freq)
            score += idf_score * (f * (k1 + 1)) / \
                (f + k1 * (1 - b + b * length / avgdl))
    return score


def main():
    directory = '../coll'  # Replace with your folder path
    results_file = 'Results.txt'
    tag = 3

    all_scores = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Parse the XML data from the file
        # I needed to slightly modify the documents the professor gave us cause I kept running into errors with her code, please us the SampleDocument.xml file for right now
        tree = BeautifulSoup(
            open(filepath, 'r').read().replace("\n", ""), 'lxml')
        # root = tree.getroot()
        doc_data = defaultdict(set)

        # Process each DOC element
        for doc in tree('doc'):
            # Find the docid and text
            doc_id = doc.find('docno').string.strip()
            # print(doc_id)

        try:
            text = doc.find('text').string.strip()
        except AttributeError:
            text = ""

        # Preprocess the text and store in the set
        processed_text = preprocess(text)
        doc_data[doc_id] = processed_text

        # Global Inverted Index
        inverted_index = {}
        # For every Doc
        for doc_id, tokens in doc_data.items():
            doc_index = buildInvertedIndex(doc_id, tokens)
            # Merge doc_index into inverted_index
            for token, postings in doc_index.items():
                if token not in inverted_index:
                    inverted_index[token] = postings
                else:
                    inverted_index[token].extend(postings)

        N = len(doc_data)
        avgdl = sum(len(doc) for doc in doc_data.values()) / N
        doc_freq = defaultdict(int)
        for doc in doc_data.values():
            for term in set(doc):
                doc_freq[term] += 1

        query = preprocess("Accusations of Cheating by Contractors on U.S. Defense Projects")
        scores = {doc_id: bm25(doc, query, N, doc_freq, avgdl)for doc_id, doc in doc_data.items()}

        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        for rank, (doc_id, score) in enumerate(ranked_docs[:1000], 1):all_scores.append(f"{1} Q0 {doc_id} {rank} {score:.4f} {tag}")

        with open(results_file, 'w') as f:
         for line in all_scores:
            f.write(line + '\n')


if __name__ == "__main__":
    main()
