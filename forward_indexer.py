import json, re, os

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import zlib
nltk.download('stopwords')


# This parses json files and creates lexicon and forward index
def generate_forward_index(path_to_data):
    start = datetime.now()

    # we create a set of stop words
    stop_words = set(stopwords.words('english'))
    snow_stemmer = SnowballStemmer(language='english')

    # check the directory for file of json format
    file_names = [posJson for posJson in os.listdir(path_to_data) if posJson.endswith('.json')]

    # if lexicon file is present we load it to memory
    if os.path.isfile('lexicon.txt'):
        prev_lexicon = open('lexicon.txt', "r")
        lexicon = json.load(prev_lexicon)
        prev_lexicon.close()
    else:
        lexicon = {"word_count": 0}

    # create a temporary document index to store record of document being indexed
    document_indices = {}
    doc_count = 0
    word_count = lexicon["word_count"]

    # load the document indices, if the file exists open in read mode and load the data then open in write mode
    if os.path.isfile('./document_index.txt'):
        with open('./document_index.txt') as doc_idx:
            document_indices = json.load(doc_idx)

    document_index = open('./document_index.txt', 'w')

    # create a list of forward barrels and we use 300 barrels
    forward_barrels = []
    for barrelCount in range(1, 301):
        forward_barrels.append(open('./forwardBarrels/forward_barrel_{}.txt'.format(barrelCount), 'w'))

    for i in range(60):
        forward_dicts = []
        for barrelCount in range(1, 301):
            forward_dicts.append({})

        file = open('{}/{}'.format(path_to_data, file_names[i]))
        loaded_data = json.load(file)
        file.close()

        # read articles in loaded data
        for article in loaded_data:

            # hash the doc id
            doc_id = bytes(article['id'], 'utf-8')
            hashedID = zlib.crc32(doc_id)

            # If the article is already indexed then continue else add doc id to document index
            if hashedID in document_indices:
                continue
            else:
                document_indices[str(hashedID)] = article['url']
                doc_count += 1

            # parse the content through regex, split it and lowercase it and then stem words in content
            content = (re.sub('[^a-zA-Z]', ' ', article['content'])).lower().split()
            stemmed_words = ([snow_stemmer.stem(word) for word in content if not word in stop_words])

            # parse the title through regex, split it and lowercase it and then stem words in title
            title = (re.sub('[^a-zA-Z]', ' ', article['title'])).lower().split()
            stemmed_title = ([snow_stemmer.stem(word) for word in title if not word in stop_words])

            position = 1  # position of word in the title
            # store the title words in the hit list
            for word in stemmed_title:

                # add word to lexicon if not in lexicon
                if word not in lexicon:
                    lexicon[word] = word_count
                    word_count += 1

                # through word_id calculate which barrel it belongs to and then add hitlist for title
                barrelLocation = int(lexicon[word] / 533)
                if (hashedID, lexicon[word]) not in forward_dicts[barrelLocation]:
                    # here hitlist consist of two sub lists, first list for title and second for content
                    # in title hitlist, first element is always 1 and second element is hit count
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])] = []
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])].insert(0, [1, 1])
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])].insert(1, [0, 0])
                else:
                    # if hit list is present we just increase hit count for title hits
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])][0][1] += 1
                position += 1

            position = 1  # position of word in the document

            for word in stemmed_words:

                if word not in lexicon:
                    lexicon[word] = word_count
                    word_count += 1

                barrelLocation = int(lexicon[word] / 533)
                if (hashedID, lexicon[word]) not in forward_dicts[barrelLocation]:
                    # in content hitlist, first element is always 0 and second element is hit count
                    # and then hit position are appended
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])] = []
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])].insert(0, [1, 0])
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])].insert(1, [0, 1, position])
                else:
                    # if hit list is present we just increase hit count for content hits
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])][1][1] += 1
                    forward_dicts[barrelLocation][(hashedID, lexicon[word])][1].append(position)
                position += 1

        id = 0
        while id < 300:  # here 300 is barrel count
            # write content of forward dictionary to corresponding forward barrels
            for object in forward_dicts[id].items():
                forward_barrels[id].write(json.dumps(object))
                forward_barrels[id].write("\n")
            id += 1

    # dump lexicon program which updates previous lexicon to create new lexicon
    lexicon["word_count"] = word_count
    new_lexicon = open('lexicon.txt', "w")
    new_lexicon.write(json.dumps(lexicon, indent=2))
    new_lexicon.close()

    # document indices is written to document index file
    document_index.write(json.dumps(document_indices))
    document_index.close()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is:", str(end - start))
    print('doc_count = ', doc_count)
    print('word_count = ', word_count)
