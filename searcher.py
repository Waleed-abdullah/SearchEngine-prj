import json, os
from datetime import datetime
from searchLexicon import search_lexicon


def search_word(word):
    start = datetime.now()
    offset = search_lexicon(word)
    if offset == None: 
        return None
    wordID = None
    print('offset', offset)
    with open('inverted_idx.txt', 'r') as inverted_index:
        i = 1
        for line in inverted_index:
            if i == offset:
                wordID = json.loads(line)
                break;
            i +=1
            
    
    print(wordID.keys())

    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))




