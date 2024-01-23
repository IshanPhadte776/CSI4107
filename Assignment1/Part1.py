#regular expression (regex) module in Python. Patterns used to match character combinations in strings.
import re
#Natural Language Toolkit (NLTK)
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from xml.etree import ElementTree as ET

def preprocess(document):
    # Parse the XML document
    root = ET.fromstring(document)
    
    # Extract the text content from the TEXT element
    text_element = root.find(".//TEXT")
    text = text_element.text if text_element is not None else ""

    # Remove markup that is not part of the text
    text = re.sub(r'<.*?>', '', text)

    # Tokenization - Split the text into words
    tokens = re.findall(r'\b\w+\b', text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Optional: Use Porter Stemmer for stemming
    porter = PorterStemmer()
    tokens = [porter.stem(word) for word in tokens]

    return tokens

# def build_inverted_index(doc_id, tokens):

#     inverted_index = {}

#     for position, token in enumerate(tokens):
#         if token not in inverted_index:
#             inverted_index[token] = [(doc_id, position)]
#         else:
#             inverted_index[token].append((doc_id, position))
#     return inverted_index



# Read the XML document from a file
with open("SampleDocument.xml", "r") as file:
    xml_content = file.read()

# Preprocess the document
processed_tokens = preprocess(xml_content)
print(processed_tokens)


#uildInvertedIndex()
