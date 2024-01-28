#regular expression (regex) module in Python. Patterns used to match character combinations in strings.
import re
#Natural Language Toolkit (NLTK)
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from xml.etree import ElementTree as ET
from collections import defaultdict

def preprocess(text):
    # Parse the XML document
    #root = ET.fromstring(document)
    
    # Extract the text content from the TEXT element
    #text_element = root.find(".//TEXT")
    #text = text_element.text if text_element is not None else ""

    # Remove markup that is not part of the text
    text = re.sub(r'<.*?>', '', text)

    # Tokenization - Split the text into words
    tokens = re.findall(r'\b\w+\b', text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    #Don't use Porter Stemmer, it cuts some words off incorrectly, (Cut officers to offic)
    #Using Porter does feel to speed up the code 
    # porter = PorterStemmer()
    # tokens = [porter.stem(word) for word in tokens]

    return tokens

def buildInvertedIndex(doc_id, tokens):

    inverted_index = {}

    for position, token in enumerate(tokens):
        if token not in inverted_index:
            inverted_index[token] = [(doc_id, position)]
        else:
            inverted_index[token].append((doc_id, position))
    return inverted_index

# Parse the XML data from the file
tree = ET.parse('SampleDocument.xml')

print(tree)


root = tree.getroot()

print(root)
# Use a defaultdict to store results with DocID as key and processed text as values
doc_data = defaultdict(set)

# Process each DOC element
for doc in root.findall('.//DOC'):
    doc_id = doc.find('DOCNO').text.strip()
    text = doc.find('TEXT').text.strip()

    

    # Preprocess the text and store in the set
    processed_text = preprocess(text)
    doc_data[doc_id] = processed_text

# Now, doc_data is a defaultdict with DocID as keys and sets of tokens as values
# You can access the data like doc_data['AP880212-0001']

# Print the results
# for doc_id, tokens in doc_data.items():
#     print(f"DocID: {doc_id}")
#     print("Tokens:", tokens)
#     print("\n")


inverted_index = buildInvertedIndex(1, processed_tokens)

print(inverted_index)