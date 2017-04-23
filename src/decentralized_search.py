import networkx as nx
import random


class HierarchicalDecentralizedSearch:
    def __init__(self, G, hierarchy):
        """
        Initializations for hierarchy-based decentralized search, which requires a graph of nodes and a hierarchy
        that expresses "distance" between any pair of nodes
        """
        self.G = G
        self.hierarchy = hierarchy

    def get_hierarchy_distance(self, node1, node2):
        """
        Gets the distance between two nodes in the hierarchy
        """
        return len(nx.shortest_path(self.hierarchy, source=node1, target=node2))

    def get_decentralized_search_path(self, node1, node2):
        """
        Uses decentralized search to get the path between two given nodes
        """
        print(node1.name + " to " + node2.name)
        current_node = node1
        decentralized_search_path = []
        decentralized_search_path.append(current_node)
        visited_nodes = set()
        while current_node != node2:
            current_neighbors = self.G.neighbors(current_node)
            min_distance = float("inf")
            min_distance_node = None
            for neighbor in current_neighbors:
                if len(neighbor.categories) > 0 and (neighbor not in visited_nodes):
                    current_distance = self.get_hierarchy_distance(current_node, neighbor)
                    if current_distance < min_distance:
                        min_distance = current_distance
                        min_distance_node = neighbor
            if min_distance_node is None:
                while (min_distance_node is None) or (len(min_distance_node.categories) == 0):
                    min_distance_node = current_neighbors[random.randint(0, len(current_neighbors) - 1)]
            decentralized_search_path.append(min_distance_node)
            current_node = min_distance_node
            visited_nodes.add(current_node)
        return decentralized_search_path

    def run_decentralized_search(self, num_times):
        """
        Runs decentralized search the specified number of times (num_times) by randomly selecting a pair of nodes
        for each run
        """
        nodes = self.G.nodes()
        decentralized_search_paths = []
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
            search_path = self.get_decentralized_search_path(node1, node2)
            print("Decentralized Search " + str(i + 1) + ": Length " + str(len(search_path)))
            decentralized_search_paths.append(search_path)
        mean_path_length = 0.0
        for search_path in decentralized_search_paths:
            mean_path_length += len(search_path)
        mean_path_length = float(mean_path_length) / len(decentralized_search_paths)
        print ("Mean Path Length of Decentralized Search " + str(mean_path_length))




