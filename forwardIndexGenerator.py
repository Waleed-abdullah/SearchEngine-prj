import json, re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime
from parseJson import *
from dumpLexicon import dumpLexicon


# This parses json files and creates forward index and inverted index
def generateFwdIdx(pathToData):

    start = datetime.now()

    stopWords = set(stopwords.words('english'))
    snowStemmer = SnowballStemmer(language='english')

    fileNames = getJsonFileNames(pathToData)

    forwardIndex = open("forward_index.txt", 'w')
    lexicon = {}

    for i in range(1):

        LoadedData = readJsonData(fileNames[i])

        for article in LoadedData:
            docID = article['id']
            content = (re.sub('[^a-zA-Z]', ' ', article['content'])).lower().split()
            stemmedWords = ([snowStemmer.stem(word) for word in content if not word in stopWords])
            
            position = 1 # position of word in the document

            forwardDict = {}
            hitList = {}

            for word in stemmedWords:
                if word not in hitList:
                    hitList[word] = [1, position]
                else:
                    hitList[word][0] += 1
                    hitList[word].append(position)
                position += 1
                if word not in lexicon:
                    lexicon[word] = 0

            forwardDict[docID] = hitList
            forwardIndex.write(json.dumps(forwardDict))

        dumpLexicon(lexicon)

    forwardIndex.close()

    end = datetime.now()
    print("The time of execution of to create forward index and lexicon is :", str(end - start))


