import json, os

def generate_inverted_index():
   
    prev_lex_file = open('lexicon.txt', 'r')
    lexicon = json.load(prev_lex_file)
    prev_lex_file.close()
    # putting an arbitrary value at list[0] so that we can use 1 ... n
    invertex_idx = []

    with open('forward_index.txt', 'r') as fwd_idx:
        for object in fwd_idx:
            document = json.load(object)
            docID = document.keys()[0]
            hitList = document[docID]
            for word, hits in hitList:
                if lexicon[word]:
                    invertex_idx[lexicon[word] - 1][word].append([docID, hits])
                else:
                    invertex_idx.append({word: []})
                    lexicon[word] = len(invertex_idx) - 1

    new_lexicon = open('lexicon.txt', 'w')
    new_lexicon.write(json.dumps(lexicon))
    new_lexicon.close()    

    if not os.path.isfile('./inverted_idx.txt'):
            inverted_idx = open('inverted_idx.txt', 'w')
    else:
        inverted_idx = open('inverted_idx.txt', 'a')




