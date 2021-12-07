import os, json, re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

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
            raw_data = data_load[i]['content']
            words = (re.sub('[^a-zA-Z]', ' ', raw_data)).lower().split()
            processed_data = [snow_stemmer.stem(word) for word in words if not word in set(stopwords.words('english'))]
            for x in processed_data:
                f.write(x + "\n")
            i = i+1

parse_json()
