import json, os


# this takes the new words in form of dict as input and creates a new lexicon file with the additions
def dumpLexicon(input_dict):
    if os.path.isfile('lexicon.txt'):
        prev_lexicon = open('lexicon.txt', "r")
        data = json.load(prev_lexicon)
        for x in input_dict:
            if x not in data:
                data[x] = 0
        prev_lexicon.close()
    else:
        data = {}
        for x in input_dict:
            data[x] = 0
    new_lexicon = open('lexicon.txt', "w")
    new_lexicon.write(json.dumps(data))
    new_lexicon.close()