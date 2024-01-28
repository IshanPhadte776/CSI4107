#The Code Shouldn't take more than 5 Seconds to Run 

#regular expression (regex) module in Python. Patterns used to match character combinations in strings.
import re
#Natural Language Toolkit (NLTK)
import nltk
#Stopwords are like basic non-special words
from nltk.corpus import stopwords
#Imported just incase someone wanted to use it 
from nltk.stem import PorterStemmer
#For parsing
from xml.etree import ElementTree as ET
#For Dictionaries
from collections import defaultdict

#Part 1
def preprocess(text):
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

#Part 2
#Creates the inverted index for 1 document
def buildInvertedIndex(doc_id, tokens):
    inverted_index = {}

    #For every token(word)    
    for position, token in enumerate(tokens):
        #Add the token to inverted index / position
        if token not in inverted_index:
            inverted_index[token] = [(doc_id, position)]
        else:
            inverted_index[token].append((doc_id, position))

    return inverted_index


# Parse the XML data from the file
#I needed to slightly modify the documents the professor gave us cause I kept running into errors with her code, please us the SampleDocument.xml file for right now
tree = ET.parse('SampleDocument.xml')

#Get the root
root = tree.getroot()

# Use a defaultdict to store results with DocID as key and processed text as values
doc_data = defaultdict(set)

# Process each DOC element
for doc in root.findall('.//DOC'):
    #Find the docid and text
    doc_id = doc.find('DOCNO').text.strip()
    text = doc.find('TEXT').text.strip()

    # Preprocess the text and store in the set
    processed_text = preprocess(text)
    doc_data[doc_id] = processed_text

#Global Inverted Index    
inverted_index = {}
#For every Doc
for doc_id, tokens in doc_data.items():
    doc_index = buildInvertedIndex(doc_id, tokens)
    # Merge doc_index into inverted_index
    for token, postings in doc_index.items():
        if token not in inverted_index:
            inverted_index[token] = postings
        else:
            inverted_index[token].extend(postings)

print(inverted_index)

#Part 3 Goes Here