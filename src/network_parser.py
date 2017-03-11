import xmltodict


def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:  # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d

d = convert('../data/nogamenolife_pages_current.xml')

import networkx

class NetworkParser:
    def __init__(self): #TODO any settings for the network parser
        pass

    def generate_graph(self, dict):
        pass

if __name__ == '__main__':



