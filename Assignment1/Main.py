import os
import re
import nltk
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ProcessPoolExecutor

# nltk.download('stopwords')

def preprocess(text):
    text = re.sub(r'<.*?>', '', text)
    tokens = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def process_document(filepath):
    tree = BeautifulSoup(open(filepath, 'r').read().replace("\n", " "), 'lxml')

    doc_data = defaultdict(set)

    for doc in tree('doc'):
        doc_id = doc.find('docno').string.strip()

        try:
            text = doc.find('text').string.strip()
        except AttributeError:
            text = ""

        processed_text = preprocess(text)
        doc_data[doc_id] = processed_text

    return doc_data

def build_inverted_index(doc_id, tokens):
    inverted_index = {}

    for position, token in enumerate(tokens):
        if token not in inverted_index:
            inverted_index[token] = [(doc_id, position)]
        else:
            inverted_index[token].append((doc_id, position))

    return inverted_index

def perform_search(query, doc_data_list):
    inverted_index = {}
    all_documents = []

    for doc_data in doc_data_list:
        for doc_id, tokens in doc_data.items():
            doc_index = build_inverted_index(doc_id, tokens)

            for token, postings in doc_index.items():
                if token not in inverted_index:
                    inverted_index[token] = postings
                else:
                    inverted_index[token].extend(postings)

        # Convert the doc_data values (processed text) to a list
        all_documents.extend([" ".join(doc) for doc in doc_data.values()])

    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_documents)

    query_vector = vectorizer.transform([" ".join(query)])

    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    sorted_documents = sorted(zip(doc_data.keys(), cosine_similarities), key=lambda x: x[1], reverse=True)

    return sorted_documents

def write_results(sorted_documents, output_file='Results.txt'):
    all_results = []
    query_number = 0
    counter = 1

    for doc_id, score in sorted_documents:
        all_results.append(f"{query_number} , Q0 , {doc_id} {counter} {score:.4f}, run_name")
        counter += 1

    with open(output_file, 'w') as file:
        for result in all_results:
            file.write(result + '\n')

def main():
    start = time.time()
    directory = './coll'

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_document, os.path.join(directory, filename)) for filename in os.listdir(directory)]
        doc_data_list = [future.result() for future in futures]

    sorted_documents = perform_search("Accusations of Cheating by Contractors on U.S. Defense Projects", doc_data_list)

    write_results(sorted_documents)

    print("--- %s seconds ---" % (time.time() - start))

if __name__ == "__main__":
    main()
