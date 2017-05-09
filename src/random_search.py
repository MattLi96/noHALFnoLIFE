import random
from collections import Counter

import networkx as nx

from settings import path_length_cap


class RandomSearch:
    def __init__(self, G, network_analysis):
        """
        Initializations for hierarchy-based decentralized search, which requires a graph of nodes and a hierarchy
        that expresses "distance" between any pair of nodes
        """
        self.G = G.copy()
        self.network_analysis = network_analysis

    def get_search_path(self, node1, node2):
        """
        Uses decentralized search to get the path between two given nodes
        """
        last_node = None
        current_node = node1
        search_path = [current_node]
        visited_edges, unique_pages = set(), set()

        target_zone = set()
        target_zone.add(node2)

        unique_pages.add(current_node)
        while current_node != node2:
            if len(search_path) >= path_length_cap:  # Hardcap path length
                return None

            next_node = None
            current_neighbors = self.G.neighbors(current_node)
            if node2 in current_neighbors:
                next_node = node2
            else:
                options = list(set(current_neighbors) - set(unique_pages))
                if len(options) > 0:
                    next_node = random.choice(options)

            if next_node is None:
                if len(current_neighbors) == 0:
                    # Pop this page and return to the last page
                    next_node = last_node
                else:
                    next_node = random.choice(current_neighbors)
            search_path.append(next_node)
            visited_edges.add((current_node, next_node))
            last_node = current_node
            current_node = next_node
            unique_pages.add(current_node)
        return (search_path, unique_pages)

    def run_search(self, num_times, plots):
        """
        Runs randomized search the specified number of times (num_times) by randomly selecting a pair of nodes
        for each run
        """
        nodes = self.G.nodes()
        search_paths = []
        search_paths_unique_nodes = []
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
            results = self.get_search_path(node1, node2)
            if results is None:
                search_path = None
                search_path_unique_nodes = None
            else:
                search_path, search_path_unique_nodes = results
                print("Random Search " + str(i + 1) + ": Length " + str(len(search_path)))

            search_paths.append(search_path)
            search_paths_unique_nodes.append(search_path_unique_nodes)

        # Calculate mean path length
        mean_path_length = 0.0
        num_paths_found = 0
        path_distribution = []

        for search_path in search_paths:
            if search_path is not None:
                path_distribution.append(len(search_path))
                mean_path_length += len(search_path)
                num_paths_found = num_paths_found + 1
        mean_path_length = float(mean_path_length) / num_paths_found

        # Path Length Distribution
        distro = sorted(Counter(path_distribution).items())
        xdata = list(map(lambda x: x[0], distro))
        ydata = list(map(lambda x: x[1], distro))
        ydata = [float(i) / sum(ydata) for i in ydata]

        cdf = [0] * len(ydata)
        for i in range(0, len(ydata)):
            cdf[i] = sum(ydata[:i + 1])

        if plots:
            self.network_analysis.makePlot("Random Path Distribution", "Path Length", "Occurances", xdata, ydata,
                "random_path_pdf.png")
            self.network_analysis.makePlot("CDF of Random Path Distribution", "Path Length", "Occurances", xdata,
                cdf, "random_path_cdf.png")
            self.network_analysis.write_data_json("cdfdump.json", dict(zip(xdata, cdf)))

        # Calculate mean unique nodes for each path
        mean_unique_nodes = 0.0
        for path_unique_nodes in search_paths_unique_nodes:
            if path_unique_nodes is not None:
                mean_unique_nodes += len(path_unique_nodes)
        mean_unique_nodes = float(mean_unique_nodes) / num_paths_found
        print("Num Paths Found:", num_paths_found)
        print("Num Paths Not Found:", len(search_paths) - num_paths_found)
        print("Mean Path Length of Randomized Search:", mean_path_length)
        print("Mean Unique Nodes of Path of Randomized Search:", mean_unique_nodes)
        return num_paths_found, len(search_paths) - num_paths_found, mean_path_length, mean_unique_nodes
