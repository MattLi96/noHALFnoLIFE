import json
import networkx as nx
from networkx.readwrite import json_graph

class DataDump:
    def __init__(self, G):  # TODO any settings for the network parser
        self.G = G

        # Augment Graph with Metadata
        for ix,deg in G.degree().items():
            G.node[ix]['degree'] = deg
            G.node[ix]['parity'] = (1-deg%2)

        for ix,katz in nx.katz_centrality(G).items():
            G.node[ix]['katz'] = katz

        G.nodes(data=True)

    def dump(self, outfile):
        data = json_graph.node_link_data(self.G)
        with open(outfile, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == '__main__':
    pass
