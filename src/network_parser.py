import re

import networkx as nx


class Node:
    def __init__(self, name, categories=None):
        """
        Constructor for initializing a node/page in a wikia
        ----------
        name - string that should be the title of the page
        categories - set of categories that this page has been tagged with
        """
        self.name = name
        if categories is None:
            self.categories = list()
        else:
            self.categories = categories
        self.neighbor_to_location = dict()  # mapping from each neighbor node's name to its index/location on the page

    def __repr__(self):
        return self.name


class NetworkParser:
    def __init__(self, d):  # TODO any settings for the network parser
        self.G = self.createGraphFromDict(d)
        self.d = d

    def createGraphFromDict(self, d):
        """
        Creates a network of the wikia by creating a node for each page and corresponding edges between nodes
        that represent links
        ----------
        d - dictionary of pages in the wikia mapping page name to the page's text content
        """
        G = nx.DiGraph()
        name_to_node = {}
        for key in d:
            current_node = Node(key)
            name_to_node[key] = current_node
            G.add_node(current_node)

        for node in G.nodes():
            links = self.getLinksFromText(d[node.name])
            current_link_index = 0
            for link in links:
                if link.startswith("Category:"):
                    node.categories.append(link[link.find(":") + 1:])
                if link in name_to_node:
                    node.neighbor_to_location[link] = current_link_index
                    current_link_index += 1

            link_set = set()
            edge_list = []
            counter = 0
            for l in links:
                if l in name_to_node and l not in link_set:
                    link_set.add(l)
                    edge_list.append((node, name_to_node[l], {'page_loc': counter}))
                    counter += 1
            G.add_edges_from(edge_list)

        return G

    def getLinksFromText(self, text):
        bracketed_links = re.findall('\[\[.*?\]\]', text)
        cleaned_links = []
        for link in bracketed_links:
            if '|' in link:
                new_link = link[2:len(link) - 2].split('|')[0].strip()
                cleaned_links.append(new_link)
            else:
                cleaned_links.append((link[2:len(link) - 2]).strip())
        return cleaned_links


if __name__ == '__main__':
    pass
