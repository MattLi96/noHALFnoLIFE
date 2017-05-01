import networkx as nx
import random
import os
from collections import Counter
import matplotlib.pyplot as plt

class HierarchicalDecentralizedSearch:
    def __init__(self, G, hierarchy, detailed_print=True, hierarchy_nodes_only=True):
        """
        Initializations for hierarchy-based decentralized search, which requires a graph of nodes and a hierarchy
        that expresses "distance" between any pair of nodes
        """
        if hierarchy_nodes_only:
            i = 0
            total_nodes = len(G.nodes())
            for node in G.nodes():
                if len(node.categories) == 0:
                    G.remove_node(node)
                    i += 1
            print ("Performing decentralized search only on pages in the hierarchy (" + str(total_nodes - i) +
                   " of " + str(total_nodes) + " nodes)")
        self.G = G
        self.hierarchy = hierarchy
        self.detailed_print = detailed_print

    def get_hierarchy_distance(self, node1, node2):
        """
        Gets the distance between two nodes in the hierarchy
        """
        return len(nx.shortest_path(self.hierarchy, source=node1, target=node2))

    def get_decentralized_search_path(self, node1, node2, widen_target):
        """
        Uses decentralized search to get the path between two given nodes
        """
        if self.detailed_print:
            print("\n" + node1.name + " to " + node2.name)

        last_node = None
        current_node = node1
        decentralized_search_path = [current_node]
        visited_edges, unique_pages = set(), set()

        target_zone = set()
        target_zone.add(node2)

        if widen_target:
            all_nodes = list(map(lambda x: (x, self.get_hierarchy_distance(x, node2)), self.G.nodes()))
            sorted_by_hierarchy = sorted(all_nodes, key=lambda tup: tup[1])
            for i in range(0,3):
                if self.detailed_print:
                    print(sorted_by_hierarchy[i])
                target_zone.add(sorted_by_hierarchy[i][0])

            # If you know the neighbors
            # target_zone.update(self.G.neighbors(node2))
        if self.detailed_print:
            print("TARGET ZONE: " + str(target_zone))

        unique_pages.add(current_node)
        while current_node != node2:
            if len(decentralized_search_path) >= len(self.G.nodes()):
                return None
            if self.detailed_print:
                try:
                    print ("CURRENT NODE: " + str(current_node) + " , DISTANCE: " +
                           str(self.get_hierarchy_distance(current_node, node2)))
                except Exception as e:
                    print("CURRENT NODE: " + str(current_node))

            current_neighbors = self.G.neighbors(current_node)
            min_distance = float("inf")
            min_distance_node = None
            equal_distance_nodes = []
            if self.detailed_print:
                print("CURRENT NEIGHBORS: " + str(list(map(lambda x: (x, self.get_hierarchy_distance(x, node2)), current_neighbors))))

            for neighbor in current_neighbors:
                # Check if a neighbor is the destination node before utilizing the hierarchical scores
                if neighbor == node2:
                    min_distance_node = neighbor
                    break
                elif len(neighbor.categories) > 0 and ((current_node, neighbor) not in visited_edges):
                    # Try to use more than just hierarchy
                    try:
                        current_distance = self.get_hierarchy_distance(neighbor, node2)
                        current_distance_target = list(map(lambda x: self.get_hierarchy_distance(neighbor, x), target_zone))
                        target_min = min(current_distance_target)

                        current_distance = min(current_distance, target_min)
                    except Exception as e:
                        continue
                    if current_distance == min_distance:
                        equal_distance_nodes.append(neighbor.name)
                    if current_distance < min_distance:
                        equal_distance_nodes = []
                        min_distance = current_distance
                        min_distance_node = neighbor
            if self.detailed_print:
                print("OTHER POSSIBILITIES: " + str(equal_distance_nodes) + "\n")
            if min_distance_node is None:
                if len(current_neighbors) == 0:
                    # Pop this page and return to the last page
                    min_distance_node = last_node
                elif len(current_neighbors) == 1:
                    min_distance_node = current_neighbors[0]
                else:
                    while (min_distance_node is None) or (len(min_distance_node.categories) == 0):
                        min_distance_node = current_neighbors[random.randint(0, len(current_neighbors) - 1)]
            decentralized_search_path.append(min_distance_node)
            visited_edges.add((current_node, min_distance_node))
            last_node = current_node
            current_node = min_distance_node
            unique_pages.add(current_node)
        return (decentralized_search_path, unique_pages)

    def run_decentralized_search(self, num_times, widen_target):
        """
        Runs decentralized search the specified number of times (num_times) by randomly selecting a pair of nodes
        for each run
        """
        nodes = self.G.nodes()
        decentralized_search_paths = []
        decentralized_search_paths_unique_nodes = []
        for i in range(num_times):
            node1 = None
            node2 = None
            while (node1 is None) or (node2 is None) or (nx.has_path(self.G, node1, node2) == False):
                while True:
                    rand1_index = random.randint(0, len(nodes) - 1)
                    if len(nodes[rand1_index].categories) > 0:
                        node1 = nodes[rand1_index]
                        break
                while True:
                    rand2_index = random.randint(0, len(nodes) - 1)
                    if rand2_index != rand1_index and len(nodes[rand2_index].categories) > 0:
                        node2 = nodes[rand2_index]
                        break
            results = self.get_decentralized_search_path(node1, node2, widen_target)
            if results is None:
                search_path = None
                search_path_unique_nodes = None
                if self.detailed_print:
                    print ("Couldn't find path for " + str(i + 1))
            else:
                search_path, search_path_unique_nodes = results
                if self.detailed_print:
                    print(str(search_path))
                    print("Decentralized Search " + str(i + 1) + ": Length " + str(len(search_path)))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                else:
                    print("Decentralized Search " + str(i + 1) + ": Length " + str(len(search_path)))

            decentralized_search_paths.append(search_path)
            decentralized_search_paths_unique_nodes.append(search_path_unique_nodes)

        # Calculate mean path length
        mean_path_length = 0.0
        num_paths_found = 0
        path_distribution = []

        for search_path in decentralized_search_paths:
            if search_path is not None:
                path_distribution.append(len(search_path))
                mean_path_length += len(search_path)
                num_paths_found = num_paths_found + 1
        mean_path_length = float(mean_path_length) / num_paths_found

        # Path Length Distribution
        distro = sorted(Counter(path_distribution).items())
        xdata = list(map(lambda x: x[0],distro))
        ydata = list(map(lambda x: x[1],distro))
        ydata = [float(i)/sum(ydata) for i in ydata]

        cdf = [0]*len(ydata)
        for i in range(0, len(ydata)):
            cdf[i] = sum(ydata[:i+1])

        self.makePlot("Decentralized Path Distribution (" + str(widen_target) + ")", "Path Length", "Occurances", xdata, ydata, "./derp.png")
        self.makePlot("CDF of Decentralized Path Distribution (" + str(widen_target) + ")", "Path Length", "Occurances", xdata, cdf, "./derp2.png")

        with open('./cdfdump.json', 'w') as out:
            print(xdata)
            print(ydata)
            print(list(zip(xdata, cdf)))
            out.write('\n'.join('%s %s' % x for x in zip(xdata, cdf)))

        # Calculate mean unique nodes for each path
        mean_unique_nodes = 0.0
        for path_unique_nodes in decentralized_search_paths_unique_nodes:
            if path_unique_nodes is not None:
                mean_unique_nodes += len(path_unique_nodes)
        mean_unique_nodes = float(mean_unique_nodes) / num_paths_found
        print ("Num Paths Found: " + str(num_paths_found))
        print ("Num Paths Not Found: " + str(len(decentralized_search_paths) - num_paths_found))
        print ("Mean Path Length of Decentralized Search: " + str(mean_path_length))
        print ("Mean Unique Nodes of Path of Decentralized Search: " + str(mean_unique_nodes))

    def makePlot(self, title, xaxis, yaxis, xdata, ydata, path):
        fig = plt.figure()
        fig.suptitle(title, fontsize=14, fontweight='bold')

        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)

        ax.set_xlabel(xaxis)
        ax.set_ylabel(yaxis)

        ax.scatter(x=xdata, y=ydata)
        plt.scatter(x=xdata, y=ydata)

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        plt.savefig(path)
        plt.close()
