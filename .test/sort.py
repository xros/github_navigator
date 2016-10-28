import json
import os
HERE = os.path.dirname(__file__)
PARENT_DIR =  os.path.abspath(os.path.join(HERE, os.pardir))


with open('save.json', 'r') as f:
    # insertion sort: decreasing
    d = json.loads(f.readlines()[0])

    the_list = d['items']

    for i in range(1, len(the_list)):
        tmp = the_list[i]           # tmp is a dict obj
        k = i

        while k > 0 and tmp["created_at"] > the_list[k-1]["created_at"]:
            the_list[k] = the_list[k-1]
            the_list[k-1] = tmp
            k = k - 1
        the_list[k] = tmp

    with open('sorted.json', 'w') as ff:
        ff.write(str(the_list))
