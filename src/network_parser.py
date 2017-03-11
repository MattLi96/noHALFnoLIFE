import xmltodict
import networkx as nx
import re
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

        return G

    def getLinksFromText(self, text):
        bracketed_links = re.findall('\[\[.*?\]\]', text)
        cleaned_links = []
        for link in bracketed_links:
            cleaned_links.append((link[2:len(link)-2]).strip())
        return cleaned_links

    def convert(self):
        pass

if __name__ == '__main__':
    
    pass


