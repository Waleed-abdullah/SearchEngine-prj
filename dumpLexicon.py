import json


# this takes the new words in form of dict as input and creates a new lexicon file with the additions
def dumpLexicon(input_dict):
    prevLexicon = open('sample.txt', "r")
    data = json.load(prevLexicon)
    for x in input_dict:
        if x not in data:
            data[x] = 0
    prevLexicon.close()
    newLexicon = open('sample.txt', "w")
    newLexicon.write(json.dumps(data))
    newLexicon.close()
    