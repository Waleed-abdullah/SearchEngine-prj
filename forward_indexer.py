import os, json, re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
import time


def parse_json():
    begin = time.time()
    file_path = 'C:/Users/HP/Desktop'
    jsonFiles = [files for files in os.listdir(file_path) if files.endswith('.json')]
    snow_stemmer = SnowballStemmer(language='english')
    data = []
    stop_words = set(stopwords.words('english'))
    forward_index = open("forward_index.txt", 'w')
    for fileName in jsonFiles:
        file = open(('C:/Users/HP/Desktop/{}').format(fileName))
        data_load = json.load(file)
        i = 0
        for raw_data in data_load:
            docid = raw_data['id']
            forward_index.writelines(docid + "\n")
            text_words = list(OrderedDict.fromkeys((re.sub('[^a-zA-Z]', ' ', raw_data['content'])).lower().split()))
            temp = ([snow_stemmer.stem(word) for word in text_words if not word in stop_words])
            k = 1
            for x in temp:
                forward_index.write(x + ":" + str(k) + "  ")
                k += 1
            data += temp
            i = i+1
            forward_index.write("\n\n")
    f_lex = open("sample.txt", "w")
    for x in sorted(list(OrderedDict.fromkeys(data))):
        f_lex.write("{0:<12}\n".format(x))

    forward_index.close()
    f_lex.close()
    end = time.time()
    print(f"Total runtime of the program is {end - begin}")


parse_json()