import json, os
from datetime import datetime


def search_lexicon(word):
    file = open('lexicon.txt', "r")
    lexicon = json.load(file)
    if word not in lexicon:
        print("Word not found in lexicon\n")
        return None
    else:
        return lexicon[word]


def search_word(word):
    start = datetime.now()

    word_id = search_lexicon(word)

    if word_id is None:
        return None

    barrel_num = int(word_id[0] / 533) + 1
    inverted_index = open("./inverted_barrel_" + str(barrel_num) + ".txt", 'r')

    doc_list = []
    result_count = 1
    inverted_index.seek(word_id[1])
    line = json.loads(inverted_index.readline())
    while line[0][1] == word_id[0] and result_count < 31:
        doc_list.append([line[0][0], line[1]])
        line = json.loads(inverted_index.readline())
        result_count += 1

    print(doc_list)
    inverted_index.close()
    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))


search_word("doctor")
search_word("kashmiri")
search_word("explos")
