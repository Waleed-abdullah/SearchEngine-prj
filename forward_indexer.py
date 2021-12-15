import json, re, os
from collections import OrderedDict

import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import zlib
from sorter import ivtd_index_generator


# This parses json files and creates forward index and inverted index
def generate_forward_index(path_to_data):

    start = datetime.now()

    stop_words = set(stopwords.words('english'))
    snow_stemmer = SnowballStemmer(language='english')

    file_names = [posJson for posJson in os.listdir(path_to_data) if posJson.endswith('.json')]

    if os.path.isfile('lexicon.txt'):
        prev_lexicon = open('lexicon.txt', "r")
        lexicon = json.load(prev_lexicon)
        prev_lexicon.close()
    else:
        lexicon = {"word_count": 0}

    document_indices = {}
    doc_count = 0
    word_count = lexicon["word_count"]

    # load the document indices, if the file exists open in read mode and load the data then open in write mode
    if os.path.isfile('./document_index.txt'):
        with open('./document_index.txt') as doc_idx:
         document_indices = json.load(doc_idx)

    document_index = open('./document_index.txt', 'w')

    forward_barrel_1 = open("forward_barrel_1.txt", 'w')
    forward_barrel_2 = open("forward_barrel_2.txt", 'w')
    forward_barrel_3 = open("forward_barrel_3.txt", 'w')
    forward_barrel_4 = open("forward_barrel_4.txt", 'w')
    forward_barrel_5 = open("forward_barrel_5.txt", 'w')

    forward_barrels = [forward_barrel_1, forward_barrel_2, forward_barrel_3, forward_barrel_4, forward_barrel_5]

    for file_name in file_names:

        forward_dict_1 = {}
        forward_dict_2 = {}
        forward_dict_3 = {}
        forward_dict_4 = {}
        forward_dict_5 = {}
        forward_dicts = [forward_dict_1, forward_dict_2, forward_dict_3, forward_dict_4, forward_dict_5]

        file = open('{}/{}'.format(path_to_data, file_name))
        loaded_data = json.load(file)

        for article in loaded_data:
            doc_id = bytes(article['id'], 'utf-8')
            hashedID = str(zlib.crc32(doc_id))

            # If the article is alredy indexed then continue
            if hashedID in document_indices:
                continue
            else:
                document_indices[hashedID] = article['url']
                doc_count += 1

            content = (re.sub('[^a-zA-Z]', ' ', article['content'])).lower().split()
            stemmed_words = ([snow_stemmer.stem(word) for word in content if not word in stop_words])

            # title = (re.sub('[^a-zA-Z]', ' ', article['title'])).lower().split()
            # stemmed_title = ([snow_stemmer.stem(word) for word in title if not word in stop_words])

            # position = 1
            # # hit list structure is such that word: [0/1, occurances, position]
            # # store the title words in the hit list
            # for word in stemmed_title:
            #     if word not in hit_list:
            #         hit_list[word + str(doc_id)] = [1, 1, position]
            #     else:
            #         hit_list[word + str(doc_id)][1] += 1
            #     if word not in lexicon:
            #         lexicon[word] = 0
            #     position += 1

            position = 1  # position of word in the document

            for word in stemmed_words:

                if word not in lexicon:
                    lexicon[word] = word_count
                    word_count += 1

                if (int(hashedID), lexicon[word]) not in forward_dicts[int(lexicon[word] / 10000)]:
                    forward_dicts[int(lexicon[word] / 10000)][int(hashedID), lexicon[word]] = [0, 1, position]
                else:
                    forward_dicts[int(lexicon[word] / 10000)][(int(hashedID), lexicon[word])][1] += 1
                    forward_dicts[int(lexicon[word] / 10000)][(int(hashedID), lexicon[word])].append(position)
                position += 1

        id = 0
        count = 0
        while id < 5: # here 5 is barrel count
            for object in forward_dicts[id].items():
                forward_barrels[id].write(json.dumps(object))
                forward_barrels[id].write("\n")
                count += 1
            id += 1

    # dump lexicon
    lexicon["word_count"] = word_count
    new_lexicon = open('lexicon.txt', "w")
    new_lexicon.write(json.dumps(lexicon, indent=2))
    new_lexicon.close()

    document_index.write(json.dumps(document_indices))
    document_index.close()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is:", str(end - start))
    print(doc_count)
    print(word_count)


generate_forward_index("C:/Users/HP/Desktop/")
ivtd_index_generator()

