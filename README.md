Students:
Ishan Phadte 300238878
Lauren Gu 300320106
Angus Leung 300110509

Division of Work:

Ishan: Part 1 and Part 2 
Lauren: Part 3 
Angus: Beautiful Soup Conversion

Functionality of Program:

The program ranks the doucments based on their relevance to a given search query. This is done via the cosine similiarity
The program preprocesses XML files, creates a inverted index and uses cosine similiarity via td-idf weights 

How to run program:




Explanation of Algorithms:

Part 1

A hashmap was used because each stop word is unique, we needed a dictionary's key value pair system and needed O(1) insert and lookup

Part 2 

A Map was used for the inverted index because we needed a key value data structure and a map fits the description 

Emurating over the tokens to done so we can use the position of the tokens as a variable 

Part 3 

Dictionary is used because if duplicate keys are found, the code will act in the correct manner without errors occuring


Sample of 100 Tokens 

['nation', 'governors', 'appealed', 'whitehouse', 'sunday', 'relief', '163', 'federal', 'rules', 'regulations', 'andheard', 'former', 'governor', 'call', 'constitutional', 'convention', 'torestore', 'states', 'rights', 'new', 'hampshire', 'gov', 'john', 'h', 'sununu', 'opening', 'nationalgovernors', 'association', 'winter', 'meeting', 'said', 'time', 'hascome', 'press', 'new', 'division', 'authority', 'statesand', 'washington', 'erosion', 'fundamental', 'balance', 'struck200', 'years', 'ago', 'philadelphia', 'sununu', 'nga', 'chairman', 'said', 'ata', 'news', 'conference', 'gaveling', 'first', 'plenary', 'session', 'toorder', 'president', 'reagan', 'black', 'tie', 'dinner', 'governors', 'sundaynight', 'told', 'governors', 'envied', 'balanced', 'budgetrequirements', 'line', 'item', 'vetoes', 'many', 'possess', 'notone', 'would', 'put', 'mess', 'inwashington', 'budget', 'time', 'president', 'said', 'also', 'said', 'want', 'tie', 'successor', 'hands', 'butexpressed', 'hope', 'next', 'president', 'would', 'continue', 'tradition', 'ofinviting', 'governors', 'white']

