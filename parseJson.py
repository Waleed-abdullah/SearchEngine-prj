import os, json

# The following function returns the names of all the Json files in the directory if it ends in .json in a list
def getJsonFileNames(pathToJson):
    jsonFiles = [posJson for posJson in os.listdir(pathToJson) if posJson.endswith('.json')]
   # print(jsonFiles)
    return jsonFiles

# This function reads the json data in each corresponding file
def readJsonData(path):
    # for fileName in jsonFiles:
    file = open(path)
    data = json.load(file)
    return data
    
