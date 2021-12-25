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
   
    documents = {} 
    for word_id in word_ids:
        barrel_num = int(word_id[0] / 533) + 1
        inverted_index = open("./InvertedBarrels/inverted_barrel_" + str(barrel_num) + ".txt", 'r')

        result_count = 1
        inverted_index.seek(word_id[1])
        line = json.loads(inverted_index.readline())
        while line[0][1] == word_id[0] and result_count < 31:
            docID = str(line[0][0])
            titleHitList = line[1][0]
            titleHits = titleHitList[1]
            contentHitList = line[1][1]
            contentHits = contentHitList[1]
            if docID in documents:
                # add the new hits to the score
                    documents[docID][0] = documents[docID][0] + titleHits +  contentHits
                # calculate proximity and add weight
                    if contentHits > 0:
                        if documents[docID][1] is not None:
                            proximity = abs(documents[docID][1][2] - contentHitList[2])
                            if proximity <= 1:
                                documents[docID][0] += 10
                            elif proximity <= 10:
                                documents[docID][0] += 8
                            elif proximity <= 100:
                                documents[docID][0] += 4
                            else:
                                documents[docID][0] += 2
                        #add the hitlist of the current word for next words proximity calculation
                        documents[docID][1] = contentHitList
            else:                       
                    if contentHits > 0:
                        documents[docID] = [titleHits + contentHits, contentHitList]  # add hits in both title and content and store the hit list for proximity check
                    else:
                        documents[docID] = [titleHits + contentHits, None] 
            line = json.loads(inverted_index.readline())
            result_count += 1

        inverted_index.close()

    # convert the documents dictionary into a list and sort in descending order based on the score | higher the score the higher the rank of the document

    rankedDocuments = sorted(list(documents.items()), key = lambda x: x[1][0], reverse = True)

    print(len(rankedDocuments))
    print(rankedDocuments)
    end = datetime.now()
    print("The time of execution to search a word is:", str(end - start))


search_words(["lockdown", "protest", "retire", "civil", "signal", "quran", "opposit", "hog"])
# search_word("kashmiri")
# search_word("explos")
