
Students:
Ishan Phadte 300238878
Lauren Gu 300320106
Angus Leung 


Division of Work:

Ishan: Part 1 and Part 2 
Lauren: Part 3 
Angus: Beautiful Soup Conversion

Functionality of Program:

The program ranks the doucments based on their relevance to a given search query. This is done via the cosine similiarity
The program preprocesses XML files, creates a inverted index and uses cosine similiarity via td-idf weights 

How to run program:

- Download Python 
- Install the following libaries

nltk
beautifulsoup4
scikit-learn

Go to Main.py and run the file 

Explanation of Algorithms:

Part 1

A set was used because each stop word is unique and order isn't required

Part 2 

A Dictionary was used for the inverted index because we needed a key value data structure and a dictionary fits the description 

Emurating over the tokens to done so we can use the position of the tokens as a variable 

Part 3 

Default Dictionary is used because if duplicate keys are found, the code will act in the correct manner without errors occuring


Sample of 100 Tokens 

['nation', 'governors', 'appealed', 'whitehouse', 'sunday', 'relief', '163', 'federal', 'rules', 'regulations', 'andheard', 'former', 'governor', 'call', 'constitutional', 'convention', 'torestore', 'states', 'rights', 'new', 'hampshire', 'gov', 'john', 'h', 'sununu', 'opening', 'nationalgovernors', 'association', 'winter', 'meeting', 'said', 'time', 'hascome', 'press', 'new', 'division', 'authority', 'statesand', 'washington', 'erosion', 'fundamental', 'balance', 'struck200', 'years', 'ago', 'philadelphia', 'sununu', 'nga', 'chairman', 'said', 'ata', 'news', 'conference', 'gaveling', 'first', 'plenary', 'session', 'toorder', 'president', 'reagan', 'black', 'tie', 'dinner', 'governors', 'sundaynight', 'told', 'governors', 'envied', 'balanced', 'budgetrequirements', 'line', 'item', 'vetoes', 'many', 'possess', 'notone', 'would', 'put', 'mess', 'inwashington', 'budget', 'time', 'president', 'said', 'also', 'said', 'want', 'tie', 'successor', 'hands', 'butexpressed', 'hope', 'next', 'president', 'would', 'continue', 'tradition', 'ofinviting', 'governors', 'white']

Query 1: Coping with overcrowded prisons
Query 2:
Query 3:
Query 4:
Query 5:
Query 6:
Query 7:
Query 8:

