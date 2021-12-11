import json, re, os
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
import zlib
from dumpLexicon import dumpLexicon
from Inverted_indexer import generate_inverted_index


# This parses json files and creates forward index
def generate_forward_index(path_to_data):

    start = datetime.now()

    stop_words = set(stopwords.words('english'))
    snow_stemmer = SnowballStemmer(language='english')

    file_names = [posJson for posJson in os.listdir(path_to_data) if posJson.endswith('.json')]

    forward_index = open("forward_index.txt", 'w')
    lexicon = {}
    documentIndices = {}

    # load the document indices, if the file exists open in read mode and load the data then open in write mode
    if os.path.isfile('./document_index.txt'):
       with open('./document_index.txt') as doc_idx:
            documentIndices = json.load(doc_idx)
    
    
    document_Index = open('./document_index.txt', 'w')

    # generate the forward index
    for i in range(1):
        file = open('./Dataset/nela-gt-2020/newsdata/abcnews.json')
        #file = open('{}/{}'.format(path_to_data, fileName))
        loaded_data = json.load(file)

        for article in loaded_data:
            doc_id = bytes(article['id'], 'utf-8')
            hashedID = str(zlib.crc32(doc_id))

           # If the article is alredy indexed then continue
            if hashedID in documentIndices:
                continue
            else:
                documentIndices[hashedID] = article['url']    

            content = (re.sub('[^a-zA-Z]', ' ', article['content'])).lower().split()
            title = (re.sub('[^a-zA-Z]', ' ', article['title'])).lower().split()
            stemmed_words = ([snow_stemmer.stem(word) for word in content if not word in stop_words])
            stemmed_title = ([snow_stemmer.stem(word) for word in title if not word in stop_words])

            forward_dict = {}
            hit_list = {}

            # hit list structure is such that word: [0/1, occurances, position]
            # store the title words in the hit list
            for word in stemmed_title:
                if word not in hit_list:
                    hit_list[word] = [1, 1, 0]
                else:
                    hit_list[word][1] += 1
                if word not in lexicon:
                    lexicon[word] = 0   

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

        dumpLexicon(lexicon)

    forward_index.close()
    document_Index.write(json.dumps(documentIndices))
    document_Index.close()
    generate_inverted_index()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is:", str(end - start))




    