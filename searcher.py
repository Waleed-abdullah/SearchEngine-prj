import json, os
from datetime import datetime
from searchLexicon import search_lexicon


def search_word(word):
    start = datetime.now()

    word_id = search_lexicon(word)

    if word_id is None:
        return None

    barrel_num = int(word_id / 533) + 1
    inverted_index = open("./inverted_barrel_" + str(barrel_num) + ".txt", 'r')

    doc_list = []
    line = json.loads(inverted_index.readline())
    while line[0][1] != word_id:
        line = json.loads(inverted_index.readline())
    while line[0][1] == word_id:
        doc_list.append([line[0][0], line[1]])
        line = json.loads(inverted_index.readline())

    print(doc_list)
    inverted_index.close()
    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))


search_word("vetothebil")
#search_word("delhi")
search_word("undoctor")
search_word("kashmiri")
