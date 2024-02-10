import re
import os
import concurrent.futures
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Part 1: Preprocessing
def preprocess(text):
    text = re.sub(r'<.*?>', '', text)
    tokens = re.findall(r'\b\w+\b', text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Part 2: Build Inverted Index for a Document
def build_inverted_index(doc_id, tokens):
    inverted_index = {}
    for position, token in enumerate(tokens):
        if token not in inverted_index:
            inverted_index[token] = [(doc_id, position)]
        else:
            inverted_index[token].append((doc_id, position))
    return inverted_index

# Part 3: Process Documents and Build Global Inverted Index
def process_document(filepath):
    tree = BeautifulSoup(open(filepath, 'r').read().replace("\n", " "), 'lxml')
    
    doc_data = defaultdict(list)
    
    for doc in tree('doc'):
        doc_id = doc.find('docno').string.strip()
        
        try:
            text = doc.find('text').string.strip()
        except AttributeError:
            text = ""
        
        processed_text = preprocess(text)
        doc_data[doc_id] = processed_text
    
    return doc_data

def process_documents(directory):
    all_results = []
    doc_data = defaultdict(list)
    filepaths = [os.path.join(directory, filename) for filename in os.listdir(directory)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_document, filepaths))

    for result in results:
        for doc_id, tokens in result.items():
            doc_data[doc_id] = tokens

    inverted_index = {}
    for doc_id, tokens in doc_data.items():
        doc_index = build_inverted_index(doc_id, tokens)
        for token, postings in doc_index.items():
            if token not in inverted_index:
                inverted_index[token] = postings
            else:
                inverted_index[token].extend(postings)

    return doc_data, inverted_index

def perform_search(query, doc_data, inverted_index):
    query = " ".join(query)
    
    # Process the query using the same preprocessing as the documents
    processed_query = preprocess(query)

    relevant_docs = set()
    
    # Retrieve relevant documents from the inverted index
    for term in processed_query:
        if term in inverted_index:
            relevant_docs.update([posting[0] for posting in inverted_index[term]])

    # Convert relevant documents to a list for further processing
    relevant_docs = list(relevant_docs)

    # Prepare data for the TF-IDF vectorizer
    all_documents = [" ".join(doc_data[doc_id]) for doc_id in relevant_docs]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    query_vector = vectorizer.transform([query])
    
    # Calculate cosine similarities only for relevant documents
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # Sort and write results to 'Results.txt'
    sorted_documents = sorted(zip(relevant_docs, cosine_similarities), key=lambda x: x[1], reverse=True)
    
    counter = 0
    query_number = 0
    all_results = []
    
    for doc_id, score in sorted_documents:
        all_results.append(f"{query_number} , Q0 , {doc_id} {counter} {score:.4f}, run_name")
        counter += 1

    with open('Results.txt', 'w') as file:
        for result in all_results:
            file.write(result + '\n')

# Main Function
def main():

    directory = '../coll' 
    doc_data, inverted_index = process_documents(directory)

    print("Here")
    
    query = preprocess("Accusations of Cheating by Contractors on U.S. Defense Projects")
    
    perform_search(query, doc_data, inverted_index)

if __name__ == "__main__":
    main()
