# The Code Shouldn't take more than 5 Seconds to Run

# regular expression (regex) module in Python. Patterns used to match character combinations in strings.
import re
# Natural Language Toolkit (NLTK)
import nltk

import os
# Stopwords are like basic non-special words
from nltk.corpus import stopwords
nltk.download('stopwords')
# Imported just in case someone wanted to use it 
from nltk.stem import PorterStemmer
# For parsing
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

from lxml import etree

# For Dictionaries
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

directory = './coll'  

# Use a list to store results
all_results = []

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)

    # Parse the XML data from the file
    # I needed to slightly modify the documents the professor gave us cause I kept running into errors with her code, please use the SampleDocument.xml file for right now
    tree = BeautifulSoup(open(filepath, 'r').read().replace("\n", ""), 'lxml')

    # Get the root

    # If multiple parents, wrap in another tag as root

    # Use a defaultdict to store results with DocID as key and processed text as values
    doc_data = defaultdict(set)

    # Process each DOC element
    for doc in tree('doc'):
        # Find the docid and text
        doc_id = doc.find('docno').string.strip()

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

# Part 3 Goes Here
print("Part 3 running...")

query = preprocess("Accusations of Cheating by Contractors on U.S. Defense Projects")

# Convert the doc_data values (processed text) to a list
all_documents = [" ".join(doc) for doc in doc_data.values()]

# Create a TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_documents)

# Convert the query to a TF-IDF vector
query_vector = vectorizer.transform([" ".join(query)])

# Compute cosine similarities between the query and documents
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

# Sort documents based on cosine similarity
sorted_documents = sorted(zip(doc_data.keys(), cosine_similarities), key=lambda x: x[1], reverse=True)

# Append the sorted documents to the results list
for doc_id, score in sorted_documents:
    all_results.append(f"Document: {doc_id}, Cosine Similarity: {score:.4f}")

# Write the results to a text file
with open('Results.txt', 'w') as file:
    for result in all_results:
        file.write(result + '\n')

print("Results written to Results.txt")
