import json, os

def generate_inverted_index():
   
    prev_lex_file = open('lexicon.txt', 'r')
    lexicon = json.load(prev_lex_file)
    prev_lex_file.close()
    # putting an arbitrary value at list[0] so that we can use 1 ... n
    inverted_idx = []

    with open('forward_index.txt', 'r') as fwd_idx:
        for object in fwd_idx:
            document = json.loads(object)
            for docID, hitList in document.items():
                for word, hits in hitList.items():
                    if lexicon[word]:
                        inverted_idx[lexicon[word] - 1][word].append([docID, hits])
                    else:
                        inverted_idx.append({word: [[docID, hits]]})
                        lexicon[word] = len(inverted_idx)

    new_lexicon = open('lexicon.txt', 'w')
    new_lexicon.write(json.dumps(lexicon))
    new_lexicon.close()    

    if not os.path.isfile('./inverted_idx.txt'):
        inverted_idx_file = open('inverted_idx.txt', 'w')
    else:
        inverted_idx_file = open('inverted_idx.txt', 'a')

    for wordDict in inverted_idx:
        inverted_idx_file.write(json.dumps(wordDict))
        inverted_idx_file.write('\n')

generate_inverted_index()


