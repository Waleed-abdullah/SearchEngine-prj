import os, json
from datetime import datetime


def inverted_index_generator():

    start = datetime.now()
    barrels = [forward_barrel for forward_barrel in os.listdir("./forwardBarrels") if forward_barrel.startswith('forward_barrel_')]
    

    for barrel in barrels:

        forward_file = open('./forwardBarrels/{}'.format(barrel))
        inverted_list = []
        # get the barrel number corresponding to the forward index file because they are not sorted
        barrel_num = barrel[15] + barrel[16] if barrel[16].isnumeric() else barrel[15] 
        
        if os.path.isfile("./InvertedBarrels/inverted_barrel_" + barrel_num + ".txt"):
            with open("./InvertedBarrels/inverted_barrel_" + barrel_num + ".txt", 'r') as inverted_index:
                for line in inverted_index:
                    inverted_list.append(json.loads(line))

        for line in forward_file:
            inverted_list.append(json.loads(line))

        file = open("./InvertedBarrels/inverted_barrel_" + barrel_num + ".txt", 'w')
        sorted_list = sorted(inverted_list, key=lambda x: x[0][1])
        for value in sorted_list:
            file.write(json.dumps(value))
            file.write('\n')


    end = datetime.now()
    print("The time of execution of to create inverted index is:", str(end - start))

