import xmltodict
import networkx as nx
import re

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
        bracketed_links = re.findall('\[\[.*?\]\]', text)
        cleaned_links = []
        for link in bracketed_links:
            cleaned_links.append((link[2:len(link)-2]).strip())
        return cleaned_links

if __name__ == '__main__':
    pass

