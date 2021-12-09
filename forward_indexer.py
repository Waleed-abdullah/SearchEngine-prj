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

    forward_index = open("forward_index.txt", 'w')
    lexicon = {}

    for file_name in file_names:

        file = open('{}/{}'.format(path_to_data, file_name))
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

            forward_dict[zlib.crc32(doc_id)] = hit_list
            forward_index.write(json.dumps(forward_dict))

        dumpLexicon(lexicon)

    forward_index.close()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is :", str(end - start))


