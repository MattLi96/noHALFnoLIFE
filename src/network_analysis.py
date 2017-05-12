import json
import math
import os
import re
from collections import Counter
from statistics import mean

import matplotlib.pyplot as plt
import networkx as nx
from networkx.readwrite import json_graph


class NetworkAnalysis:
    def __init__(self, G, fileName, outputBase, time=None):  # TODO any settings for the network analysis
        self.G = G.copy()
        split = re.split('\\ /', fileName)
        fileName = split[0].split(".")[0]
        self.fileName = str(fileName)
        self.outputPath = outputBase + fileName + ('' if time is None else "_" + str(time.date())) + "/"
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

    def d3dump(self, output, curr_time=""):
        G = self.G.copy()
        # Augment Graph with Metadata
        for ix, deg in G.degree().items():
            G.node[ix]['degree'] = deg
            G.node[ix]['parity'] = (1 - deg % 2)
        G.nodes(data=True)
        data = json_graph.node_link_data(G)
        for node in data['nodes']:
            node['id'] = str(node['id'])
        # data['edges'] = data.pop('links')
        data['edges'] = list(map(lambda x: {"source": x[0].name, "target": x[1].name}, G.edges()))
        data['basic'] = self.returnBasicStats()
        try:
            data['basic']['averagePathLength'] = self.getAveragePathLength()
        except:
            pass

        fileName = output + self.fileName + '_' + curr_time + ".json"
        fileName = re.sub(r"\s+", '-', fileName)

        if not os.path.exists(output):
            os.makedirs(output)
        with open(fileName, 'w') as f:
            json.dump(data, f, indent=4)

        return data['basic']

    def write_data_json(self, outfile, data):
        with open(self.outputPath + outfile, 'w') as f:
            json.dump(data, f, indent=2)

    def write_permanent_data_json(self, output, data, tag=''):
        fileName = output + self.fileName + ('_' + tag if tag != '' else '') + ".json"
        fileName = re.sub(r"\s+", '-', fileName)
        if not os.path.exists(output):
            os.makedirs(output)
        with open(fileName, 'w') as f:
            json.dump(data, f, indent=2)

    def outputNodesAndEdges(self, nodesOut="nodes.txt", edgeOut="edges.txt"):
        with open(self.outputPath + nodesOut, "w", encoding="utf-8") as nodeOut, open(self.outputPath + edgeOut, "w",
                encoding="utf-8") as edgeOut:
            node_to_degree = {}
            for e in self.G.edges():
                edgeOut.write(str(e) + "\n")
                if e[0] not in node_to_degree:
                    node_to_degree[e[0]] = 0
                if e[1] not in node_to_degree:
                    node_to_degree[e[1]] = 0
                node_to_degree[e[0]] = node_to_degree[e[0]] + 1
                node_to_degree[e[1]] = node_to_degree[e[1]] + 1
            for n in self.G.nodes():
                node_degree = 0
                if n in node_to_degree:
                    node_degree = node_to_degree[n]
                nodeOut.write(str(node_degree) + ", " + str(n) + "\n")

    def generateDrawing(self, outfile="graph.pdf"):
        nx.draw_networkx(self.G, pos=nx.spring_layout(self.G), arrows=False, with_labels=False, node_size=20)
        self.outputPlt(self.outputPath + outfile)

    def returnBasicStats(self):
        res = {}
        res['numNodes'] = nx.number_of_nodes(self.G)
        res['numEdges'] = nx.number_of_edges(self.G)
        indegree = list(nx.DiGraph.in_degree(self.G).values())
        res['averageInDegree'] = mean(indegree)
        outdegree = list(nx.DiGraph.out_degree(self.G).values())
        res['averageOutDegree'] = mean(outdegree)
        res['selfLinks'] = self.G.number_of_selfloops()
        return res

    def outputBasicStats(self):
        print(self.returnBasicStats())

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
        self.makePlot('Log Histogram of Degree Frequencies', 'log j', 'log n_j', logx, logy, graphpath)

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
        self.makePlot("Nodes at Distance j", 'j', 'r_j', x, y, graphpath)

    def getAveragePathLength(self):
        try:
            return nx.average_shortest_path_length(self.G)
        except:
            # subs = nx.strongly_connected_components(self.G)
            # subLengths = list(map(lambda x: len(x), subs))
            # print(subLengths)
            try:
                subs = max(nx.strongly_connected_component_subgraphs(self.G), key=len)
                return nx.average_shortest_path_length(subs)
            except:
                return 0

    def makePlot(self, title, xaxis, yaxis, xdata, ydata, path):
        fig = plt.figure()
        fig.suptitle(title, fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.scatter(x=xdata, y=ydata)
        plt.scatter(x=xdata, y=ydata)

        self.outputPlt(self.outputPath + path)

    def outputPlt(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        plt.savefig(path)
        plt.close()

    def nodeRemoval(self):
        res = {}

        def returnBasicStats(graph):
            res = {}
            res['numNodes'] = nx.number_of_nodes(graph)
            res['numEdges'] = nx.number_of_edges(graph)
            indegree = list(nx.DiGraph.in_degree(graph).values())
            res['averageInDegree'] = mean(indegree)
            outdegree = list(nx.DiGraph.out_degree(graph).values())
            res['averageOutDegree'] = mean(outdegree)
            res['selfLinks'] = graph.number_of_selfloops()
            return res

        def getAveragePathLength(graph):
            try:
                return nx.average_shortest_path_length(graph)
            except:
                # subs = nx.strongly_connected_components(self.G)
                # subLengths = list(map(lambda x: len(x), subs))
                # print(subLengths)
                subs = max(nx.strongly_connected_component_subgraphs(graph), key=len)
                return nx.average_shortest_path_length(subs)

        def removeLargestDegree(graph):
            nlist = sorted(graph.degree_iter(), key=lambda x: x[1])
            # print(nlist)
            nodeRemove = nlist[len(nlist) - 1]
            # print(nodeRemove)
            graph.remove_node(nodeRemove[0])
            return graph, nodeRemove[0]

        G = self.G.copy()

        listComponents = sorted(nx.strongly_connected_component_subgraphs(G), key=len, reverse=True)
        largestComponentSize = len(listComponents[0])
        currentSize = largestComponentSize
        i = 0

        while currentSize > 0.5 * largestComponentSize:
            G, nodeRemoved = removeLargestDegree(G)

            startingPt = returnBasicStats(G)
            startingPt["removed"] = str(nodeRemoved)
            try:
                startingPt['averagePathLength'] = getAveragePathLength(G)
            except:
                pass

            listComponents = sorted(nx.strongly_connected_component_subgraphs(G), key=len, reverse=True)
            currentSize = len(listComponents[0])

            startingPt["sizeLargest"] = currentSize

            res[i] = startingPt
            i += 1

        self.write_data_json("nodeRemove.json", res)
        return res


if __name__ == '__main__':
    pass
