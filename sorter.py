import os, json
from datetime import datetime


def ivtd_index_generator():

    start = datetime.now()
    barrels = [forward_barrel for forward_barrel in os.listdir("./forwardBarrels") if forward_barrel.startswith('forward_barrel_')]
    barrel_count = 1

    for barrel in barrels:

        forward_file = open('./InvertedBarrels/{}'.format(barrel))
        inverted_list = []
        if os.path.isfile("./inverted_barrel_" + str(barrel_count) + ".txt"):
            with open("inverted_barrel_" + str(barrel_count) + ".txt", 'r') as inverted_index:
                for line in inverted_index:
                    inverted_list.append(json.loads(line))

        for line in forward_file:
            inverted_list.append(json.loads(line))

        file = open("inverted_barrel_" + str(barrel_count) + ".txt", 'w')
        sorted_list = sorted(inverted_list, key=lambda x: x[0][1])
        for value in sorted_list:
            file.write(json.dumps(value))
            file.write('\n')

        barrel_count += 1

    end = datetime.now()
    print("The time of execution of to create inverted index is:", str(end - start))

