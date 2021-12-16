import json, os

def counting_sort():
    arr = [[] for i in range(2500)]
    list = []
    with open('./forwardBarrels/forward_barrel_1.txt' , 'r') as barrel:
        for object in barrel:
            list.append(json.loads(object))

    for value in list:
        arr[value[0][1] % 2500].append(value)

    file = open('sample.txt', 'w')
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            file.write(json.dumps(arr[i][j]))
            file.write('\n')
counting_sort()