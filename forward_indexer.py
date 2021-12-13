import json, re, os
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import zlib
from dumpLexicon import dumpLexicon


# This parses json files and creates forward index and inverted index
def generate_forward_index(path_to_data):

    start = datetime.now()

    stop_words = set(stopwords.words('english'))
    snow_stemmer = SnowballStemmer(language='english')

    file_names = [posJson for posJson in os.listdir(path_to_data) if posJson.endswith('.json')]

    lexicon = {}
    document_indices = {}
    barrel_count = 1
    doc_count = 0

    # load the document indices, if the file exists open in read mode and load the data then open in write mode
    if os.path.isfile('./document_index.txt'):
        with open('./document_index.txt') as doc_idx:
         document_indices = json.load(doc_idx)

    document_index = open('./document_index.txt', 'w')
    forward_index = open("forward_index_barrel_" + str(barrel_count) + ".txt", 'w')

    for file_name in file_names:

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
            title = (re.sub('[^a-zA-Z]', ' ', article['title'])).lower().split()
            stemmed_words = ([snow_stemmer.stem(word) for word in content if not word in stop_words])
            stemmed_title = ([snow_stemmer.stem(word) for word in title if not word in stop_words])

            forward_dict = {}
            hit_list = {}
            position = 1

            # hit list structure is such that word: [0/1, occurances, position]
            # store the title words in the hit list
            for word in stemmed_title:
                if word not in hit_list:
                    hit_list[word] = [1, 1, position]
                else:
                    hit_list[word][1] += 1
                if word not in lexicon:
                    lexicon[word] = 0
                position += 1

            position = 1  # position of word in the document

            for word in stemmed_words:
                if word not in hit_list:
                    hit_list[word] = [0, 1, position]
                else:
                    hit_list[word][1] += 1
                    hit_list[word].append(position)
                position += 1
                if word not in lexicon:
                    lexicon[word] = 0
            forward_dict[hashedID] = hit_list
            forward_index.write(json.dumps(forward_dict))
            forward_index.write('\n')
            if doc_count % 1000 == 0:
                barrel_count += 1
                forward_index.close()
                forward_index = open("forward_index_barrel_" + str(barrel_count) + ".txt", 'w')

        dumpLexicon(lexicon)

    document_index.write(json.dumps(document_indices))
    document_index.close()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is:", str(end - start))
    print(doc_count)


