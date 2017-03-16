import json
import re

import networkx as nx

class NetworkParser:
    def __init__(self, d):  # TODO any settings for the network parser
        self.G = self.createGraphFromDict(d)
        self.d = d

    def createGraphFromDict(self, d):
        G = nx.DiGraph()
        for key in d:
            G.add_node(key)

        for key in d:
            links = self.getLinksFromText(d[key])
            edgeList = [(k, x) for (k, x) in map(lambda x: (key, x), links) if x in d]
            G.add_edges_from(edgeList)

        return G

    def getLinksFromText(self, text):
        bracketed_links = re.findall('\[\[.*?\]\]', text)
        cleaned_links = []
        for link in bracketed_links:
            cleaned_links.append((link[2:len(link) - 2]).strip())
        return cleaned_links

if __name__ == '__main__':
    pass
