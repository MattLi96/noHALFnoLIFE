import xmltodict
import networkx as nx

def convert(xml_file, xml_attribs=True):
    with open(xml_file, "rb") as f:  # notice the "rb" mode
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d

d = convert('../data/nogamenolife_pages_current.xml')

class NetworkParser:
    def __init__(self, d): #TODO any settings for the network parser
        self.G = self.createGraphFromDict(d)

    def createGraphFromDict(self, d):
        G = nx.Graph()
        for key in d:
            G.add_node(key)
            links = self.getLinksFromText(d[key])
            edgeList = map(lambda x: (key, x), links)
            G.add_edges_from(edgeList)

        return G

    def getLinksFromText(self, text):
        return

if __name__ == '__main__':
    
    pass


