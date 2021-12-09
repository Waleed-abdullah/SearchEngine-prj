import json

# returns the offset of the word in the inverted index
def searchLexicon(word):
    file = open(('lexicon.txt'))
    lexicon = json.load(file)
    if word not in lexicon:
        return None
    else:
        return lexicon[word]