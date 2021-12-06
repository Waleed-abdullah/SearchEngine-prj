import os, json

# The following function returns the names of all the Json files in the directory if it ends in .json in a list
def getJsonFileNames():
    pathToJson = './Dataset/nela-gt-2020/newsdata'
    jsonFiles = [posJson for posJson in os.listdir(pathToJson) if posJson.endswith('.json')]
   # print(jsonFiles)
    return jsonFiles

# This function reads the json data in each corresponding file
def readJsonData():
    jsonFiles = getJsonFileNames()
    
    for fileName in jsonFiles:
        file = open(('Dataset/nela-gt-2020/newsdata/{}').format(fileName))
        data = json.load(file)
        print(data[0]['id'])

readJsonData()