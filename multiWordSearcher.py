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

# receives a list of words to search
def search_words(wordsList):
    start = datetime.now()

    word_ids = []
    for word in wordsList:
        word_id = search_lexicon(word)
        if word_id is not None:
            word_ids.append(word_id)

    print(word_ids)
   
    doc_list = {} #using dict to remove duplicate documents

    for word_id in word_ids:
        barrel_num = int(word_id[0] / 533) + 1
        inverted_index = open("./InvertedBarrels/inverted_barrel_" + str(barrel_num) + ".txt", 'r')

        result_count = 1
        inverted_index.seek(word_id[1])
        line = json.loads(inverted_index.readline())
        while line[0][1] == word_id[0] and result_count < 31:
            docID = str(line[0][0])
            doc_list[docID] = doc_list.get(docID, 0) + 1 # storing the frequency of the documents in the dict
            line = json.loads(inverted_index.readline())
            result_count += 1

        inverted_index.close()


    print(len(doc_list))
    print(doc_list)
    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))


search_words(["lockdown", "protest", "retire", "civil", "signal", "quran", "opposit", "hog"])
# search_word("kashmiri")
# search_word("explos")
