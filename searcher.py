import json, os
from datetime import datetime
from searchLexicon import search_lexicon


def search_word(word):
    start = datetime.now()
    offset = search_lexicon(word)

    inverted_index = open('inverted_idx.txt', 'r')

    i = 0
    while i != offset-1:
        inverted_index.readline()
        i += 1

    doc_ids = inverted_index.readline()
    print(doc_ids)

    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))


search_word("disciplinarian")

