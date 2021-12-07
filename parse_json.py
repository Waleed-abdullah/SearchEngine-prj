import os, json, re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict

def parse_json():
    file_path = 'C:/Users/HP/Desktop'
    jsonFiles = [files for files in os.listdir(file_path) if files.endswith('.json')]
    snow_stemmer = SnowballStemmer(language='english')
    for fileName in jsonFiles:
        file = open(('C:/Users/HP/Desktop/{}').format(fileName))
        data_load = json.load(file)
        f = open("sample.txt", 'a')
        i = 0
        for raw_data in data_load:
            text_words = list(OrderedDict.fromkeys((re.sub('[^a-zA-Z]', ' ', data_load[i]['content'])).lower().split()))
            for x in sorted([snow_stemmer.stem(word) for word in text_words if not word in set(stopwords.words('english'))]):
                f.write(x + "\n")
            i = i+1
    f.close()


parse_json()

