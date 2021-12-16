import json, os

def sort(list):
    sortedList = [[] for i in range(533)]
    
    for value in list :
        sortedList[value[0][1] % 533].append(value)
        
    return sortedList