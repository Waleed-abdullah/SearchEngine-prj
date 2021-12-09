import json, re, os
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import zlib
from dumpLexicon import dumpLexicon


# This parses json files and creates forward index
def generate_forward_index(path_to_data):

    start = datetime.now()

    stop_words = set(stopwords.words('english'))
    snow_stemmer = SnowballStemmer(language='english')

    file_names = [posJson for posJson in os.listdir(path_to_data) if posJson.endswith('.json')]

    temp_forward_index = open("temp_forward_index.txt", 'w')
    lexicon = {}

    for fileName in file_names:
        file = open('{}/{}'.format(path_to_data, fileName))
        loaded_data = json.load(file)

        for article in loaded_data:
            doc_id = bytes(article['id'], 'utf-8')
            content = (re.sub('[^a-zA-Z]', ' ', article['content'])).lower().split()
            stemmed_words = ([snow_stemmer.stem(word) for word in content if not word in stop_words])

            position = 1  # position of word in the document

            forward_dict = {}
            hit_list = {}

            for word in stemmed_words:
                if word not in hit_list:
                    hit_list[word] = [1, position]
                else:
                    hit_list[word][0] += 1
                    hit_list[word].append(position)
                position += 1
                if word not in lexicon:
                    lexicon[word] = 0
            forward_dict['docID'] = zlib.crc32(doc_id)
            forward_dict['hitList'] = hit_list
            temp_forward_index.write(json.dumps(forward_dict))
            temp_forward_index.write('\n')

        dumpLexicon(lexicon)

    temp_forward_index.close()

    merge_forward_Index("temp_forward_index.txt")

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is:", str(end - start))



def merge_forward_Index(fileToBeMerged):
    # if forward index isnt already created just dump the articles
    if not os.path.isfile('forward_index.txt'):
        doc_ids = set()
        with open('forward_index.txt', 'w') as fwd_idx:
            with open(fileToBeMerged) as m:
                for object in m:
                    document = json.loads(object)
                    if document['docID'] not in doc_ids:
                        doc_ids.add(document['docID']) # in case there was a duplicate of a file/article in the dataset
                        fwd_idx.write(json.dumps(document))
                        fwd_idx.write('\n')
    else:
        doc_ids = set()
        with open('forward_index.txt', 'r+') as fwd_idx:
            for object in fwd_idx:
                document = json.loads(object)
                doc_ids.add(document['docID'])
            with open(fileToBeMerged) as m:
                for object in m:
                    document = json.loads(object)
                    if document['docID'] not in doc_ids:
                        doc_ids.add(document['docID']) # in case there was a duplicate of a file/article in the dataset
                        fwd_idx.write(json.dumps(document))
                        fwd_idx.write('\n')


    