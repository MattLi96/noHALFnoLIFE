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
        last_node = None
        current_node = node1
        decentralized_search_path = []
        decentralized_search_path.append(current_node)
        visited_edges = set()
        unique_pages = set()
        unique_pages.add(current_node)
        while current_node != node2:
            if len(decentralized_search_path) >= len(self.G.nodes()):
                return None
            print ("CURRENT NODE: " + str(current_node))
            current_neighbors = self.G.neighbors(current_node)
            print (len(current_neighbors))
            min_distance = float("inf")
            min_distance_node = None
            for neighbor in current_neighbors:
                # Check if a neighbor is the destination node before utilizing the hierarchical scores
                if neighbor == node2:
                    min_distance_node = neighbor
                    break
                elif len(neighbor.categories) > 0 and ((current_node, neighbor) not in visited_edges):
                    try:
                        current_distance = self.get_hierarchy_distance(current_node, neighbor)
                    except Exception as e:
                        continue
                    if current_distance < min_distance:
                        min_distance = current_distance
                        min_distance_node = neighbor
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
        print(len(decentralized_search_path))
        return (decentralized_search_path, unique_pages)

    def run_decentralized_search(self, num_times):
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
            results = self.get_decentralized_search_path(node1, node2)
            if results is None:
                search_path = None
                search_path_unique_nodes = None
                print ("Couldn't find path for " + str(i + 1))
            else:
                search_path, search_path_unique_nodes = results
                print("Decentralized Search " + str(i + 1) + ": Length " + str(len(search_path)))
            decentralized_search_paths.append(search_path)
            decentralized_search_paths_unique_nodes.append(search_path_unique_nodes)
        # Calculate mean path length
        mean_path_length = 0.0
        num_paths_found = 0
        for search_path in decentralized_search_paths:
            if search_path is not None:
                mean_path_length += len(search_path)
                num_paths_found = num_paths_found + 1
        mean_path_length = float(mean_path_length) / num_paths_found
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



