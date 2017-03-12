import json
import math
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph
import shutil


class NetworkAnalysis:
    def __init__(self, G, fileName):  # TODO any settings for the network analysis
        self.G = G
        split = re.split('\\ /', fileName)
        fileName = split[0].split(".")[0]
        self.fileName = fileName
        self.outputPath = "../output/" + fileName + "/"
        if os.path.exists(self.outputPath):
            shutil.rmtree(self.outputPath)
        os.makedirs(self.outputPath)

    def d3dump(self, outfile="d3dump.json"):
        G = self.G.copy()
        # Augment Graph with Metadata
        for ix, deg in G.degree().items():
            G.node[ix]['degree'] = deg
            G.node[ix]['parity'] = (1 - deg % 2)

        G.nodes(data=True)

        data = json_graph.node_link_data(G)
        with open("../public/data/" + self.fileName+".json", 'w') as f:
            json.dump(data, f, indent=4)

    def outputNodesAndEdges(self, nodesOut="nodes.txt", edgeOut="edges.txt"):
        with open(self.outputPath + nodesOut, "w") as nodeOut, open(self.outputPath + edgeOut, "w") as edgeOut:
            for n in self.G.nodes():
                nodeOut.write(n + "\n")
            for e in self.G.edges():
                edgeOut.write(str(e) + "\n")

    def generateDrawing(self, outfile="graph.png"):
        nx.draw(self.G, pos=nx.spring_layout(self.G))
        self.outputPlt(self.outputPath + outfile)

    def outputBasicStats(self):
        print(self.outputPath)
        print("# nodes: ", nx.number_of_nodes(self.G))
        print("# edges: ", nx.number_of_edges(self.G))

    def generateDegreeDistribution(self, graphpath="graphs/degreeDistribution.png"):
        output = open(self.outputPath + "degreeDistribution.txt", "w")

        degree = nx.degree(self.G)
        C = Counter(degree.values())

        maxDegree = degree[max(degree, key=lambda i: degree[i])]

        logx, logy = ([] for i in range(2))

        for i in range(0, maxDegree + 1):
            freq = C[i]
            output.write(str(i) + " " + str(freq) + "\n")
            if i > 0 and freq > 0:
                logx.append(math.log(i))
                logy.append(math.log(freq))

        output.close()
        self.makePlot('Log Histogram of Degree Frequencies', 'log j', 'log n_j', logx, logy,
                      self.outputPath + graphpath)

    def generateComponentSizes(self, graphpath="graphs/componentDistribution.png"):
        Gc = max(nx.connected_component_subgraphs(self.G), key=len)
        graphs = [graph.number_of_nodes() for graph in nx.connected_component_subgraphs(self.G)]
        C = Counter(graphs)
        maxSubgraph = Gc.number_of_nodes()

        import heapq
        res = heapq.nlargest(2, graphs)

        logx = []
        logy = []

        with open(self.outputPath + "componentDistribution.txt", "w") as output2:
            output2.write(str(maxSubgraph) + " " + str(self.G.number_of_nodes()) + " " + str(
                maxSubgraph / self.G.number_of_nodes()) + "\n")

            for i in range(0, res[1] + 1):
                output2.write(str(i) + " " + str(C[i]) + " " + "\n")
                if i > 0 and C[i] > 0:
                    logx.append(math.log(i))
                    logy.append(math.log(C[i]))
        self.makePlot('Log Histogram of Connected Components', 'log j', 'log k_j', logx, logy,
                      self.outputPath + graphpath)

    def generatePathLengths(self, start, graphpath="graphs/pathLengths.png"):
        paths = nx.single_source_dijkstra_path_length(self.G, start)
        C = Counter(paths.values())
        maxPath = paths[max(paths, key=lambda i: paths[i])]

        x = []
        y = []

        with open(self.outputPath + "pathLengths.txt", "w") as output3:
            for i in range(1, maxPath + 1):
                output3.write(str(i) + " " + str(C[i]) + "\n")
                x.append(i)
                y.append(C[i])
        self.makePlot("Nodes at Distance j", 'j', 'r_j', x, y, self.outputPath + graphpath)

    def getAveragePathLength(self):
        return nx.average_shortest_path_length(self.G)

    def makePlot(self, title, xaxis, yaxis, xdata, ydata, path):
        fig = plt.figure()
        fig.suptitle(title, fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.scatter(x=xdata, y=ydata)
        plt.scatter(x=xdata, y=ydata)

        self.outputPlt(path)

    def outputPlt(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        plt.savefig(path)
        plt.close()


if __name__ == '__main__':
    pass
