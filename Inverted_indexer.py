import json, os
from datetime import datetime

def generate_inverted_index():
    start = datetime.now()

    prev_lex_file = open('lexicon.txt', 'r')
    lexicon = json.load(prev_lex_file)
    prev_lex_file.close()
    # putting an arbitrary value at list[0] so that we can use 1 ... n
    inverted_idx = []
    if os.path.isfile('./inverted_idx.txt'):
        with open('inverted_idx.txt', 'r') as ivtd_idx:
            for object in ivtd_idx:
                inverted_idx.append(json.loads(object)) # load all the prev inverted indices

    with open('forward_index.txt', 'r') as fwd_idx:
        for object in fwd_idx:
            document = json.loads(object)
            for docID, hitList in document.items():
                for word, hits in hitList.items():
                    if lexicon[word]:
                        # using index - 1 because array indices start from 0
                        inverted_idx[lexicon[word] - 1][word].append([docID, hits]) 
                    else:
                        inverted_idx.append({word: [[docID, hits]]})
                        lexicon[word] = len(inverted_idx)

    new_lexicon = open('lexicon.txt', 'w')
    new_lexicon.write(json.dumps(lexicon))
    new_lexicon.close()    

    inverted_idx_file = open('inverted_idx.txt', 'w')

    for wordDict in inverted_idx:
        inverted_idx_file.write(json.dumps(wordDict))
        inverted_idx_file.write('\n')

    end = datetime.now()
    print("The time of execution of to create invereted Index is:", str(end - start))


