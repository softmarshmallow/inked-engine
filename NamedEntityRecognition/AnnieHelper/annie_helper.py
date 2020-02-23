
import os.path
import sys

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "../rsc/gazette.annie")


def extract_named_entity_dictionary(NE_type='OG'):
    dic = {}
    txt = open(filename, 'r').read()
    lines = txt.split("\n")
    for line in lines:
        if NE_type in line:
            items = line.split('	')
            ne = items[0]
            ne_type = items[1]
            dic[ne] = ne_type
    return dic



if __name__ == '__main__':
    dic = extract_named_entity_dictionary()
    print(dic)
