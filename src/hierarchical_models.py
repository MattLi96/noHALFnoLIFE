import networkx as nx
import numpy as np


class CategoryBasedHierarchicalModel:
    def __init__(self, G, similarity_matrix_type="cooccurrence", max_branching_factor_root=1):
        """
        Initializations for a hierarchical model based on categories of the wikia pages; note the similarity_matrix_type
        matrix specifies the type of the category similarity matrix to build, and the options are "cooccurrence" or
        "cosine similarity"
        """
        self.G = G
        self.categories = self.get_categories_set()
        # corresponds to the index of categories in the category similarity matrix
        self.index_to_category = {}
        self.category_to_index = {}
        for idx, category in enumerate(self.categories):
            self.index_to_category[idx] = category
            self.category_to_index[category] = idx
        self.ranked_categories = self.get_ranked_categories_by_degree_centrality()
        if similarity_matrix_type == "cooccurrence":
            self.category_similarity_matrix = self.get_category_similarity_matrix_by_co_occurrence()
        elif similarity_matrix_type == "cosine similarity":
            self.category_similarity_matrix = self.get_category_similarity_matrix_by_cosine_similarity()
        else:
            raise ValueError("Invalid category similarity matrix type specified")
        self.max_branching_factor = self.max_branching_factor_function(max_branching_factor_root)
        self.hierarchy = None
        self.num_hierarchy_levels = 0

    def max_branching_factor_function(self, kth_root):
        """
        Returns the max branching factor for the hierarchical model that is equal to the given kth_root of the number of
        page nodes (leaf nodes) in the hierarchy
        """
        num_hierarchy_page_nodes = 0
        for node in self.G.nodes():
            if len(node.categories) > 0:
                num_hierarchy_page_nodes += 1
        return int(pow(num_hierarchy_page_nodes, float(1) / kth_root))

    def get_categories_set(self):
        """
        Gets the set of all categories of this wikia
        """
        categories = set()
        for node in self.G.nodes():
            categories = categories.union(node.categories)
        return categories

    def get_ranked_categories_by_degree_centrality(self):
        """
        Get a ranked list of categories based on the centrality measure of degree centrality for each of the tags
        """
        category_to_centrality = {}
        for node in self.G.nodes():
            node_in_degree = self.G.in_degree(node)
            for category in node.categories:
                if category not in category_to_centrality:
                    category_to_centrality[category] = 0
                category_to_centrality[category] += node_in_degree
        return sorted(category_to_centrality, key=category_to_centrality.get, reverse=True)

    def get_category_similarity_matrix_by_cosine_similarity(self):
        """
        Builds a category similarity matrix based on the cosine similarity of the categories, where for each category
        the vector used has dimension equal to the number of pages/nodes and the ith element is 1 if the ith node has
        that category, 0 otherwise; thus the (i,j) entry in the category similarity matrix is the cosine similarity
        between the vector of the ith category and the vector of the jth category
        """
        graph_nodes = list(self.G.nodes())
        similarity_matrix_cosine = np.zeros((len(self.categories), len(self.categories)), dtype=np.float)
        category_vectors = np.zeros((len(self.categories), len(graph_nodes)), dtype=np.int)
        for i in range(len(graph_nodes)):
            for category in graph_nodes[i].categories:
                category_vectors[self.category_to_index[category]][i] = 1
        for j in range(len(category_vectors)):
            for k in range(j + 1, len(category_vectors)):
                c1 = category_vectors[j]
                c2 = category_vectors[k]
                similarity_matrix_cosine[j][k] = float(c1.dot(c2)) / (np.linalg.norm(c1) * np.linalg.norm(c2))
                similarity_matrix_cosine[k][j] = similarity_matrix_cosine[j][k]
        return similarity_matrix_cosine

    def get_category_similarity_matrix_by_co_occurrence(self):
        """
        Builds a category similarity matrix based on co-occurrence of catgories, where the (i,j) entry is the count of
        co-occurence between the ith category and the jth category
        """
        similarity_matrix_counts = np.zeros((len(self.categories), len(self.categories)), dtype=np.int)
        for node in self.G.nodes():
            node_category_list = list(node.categories)
            for i in range(len(node_category_list)):
                for j in range(i + 1, len(node_category_list)):
                    category1 = node_category_list[i]
                    category2 = node_category_list[j]
                    similarity_matrix_counts[self.category_to_index[category1]][self.category_to_index[category2]] += 1
                    similarity_matrix_counts[self.category_to_index[category2]][self.category_to_index[category1]] += 1
        return similarity_matrix_counts

    def build_hierarchical_model(self):
        """
        Builds a hierarchical model that can be used for decentralized search by using the ranked categories list (based
        on a centrality of the measure) and the category similarity matrix
        """
        self.hierarchy = nx.Graph()
        # Current categories that have been added to the hierarchy
        categories_used = set()
        # Mapping from category to its level in the hierarchy
        category_to_level = {}
        # Categories that have no child categories in the hierarchy
        leaf_categories = set()
        self.hierarchy.add_node(self.ranked_categories[0])
        category_to_level[self.ranked_categories[0]] = 0
        categories_used.add(self.ranked_categories[0])
        leaf_categories.add(self.ranked_categories[0])
        for i in range(1, len(self.ranked_categories)):
            self.hierarchy.add_node(self.ranked_categories[i])
            # Find the most similar node in hierarchy (according to the category similarity matrix) whose number of
            # children has not yet exceeded the max_branching_factor and add the current node as a child of that node
            sorted_similarity_indices = np.argsort(self.category_similarity_matrix[i])[::-1]
            similar_categories = []
            for index in sorted_similarity_indices:
                similar_categories.append(self.index_to_category[index])
            for category in similar_categories:
                if category in categories_used:
                    num_neighbors = len(self.hierarchy.neighbors(category))
                    if (category != self.ranked_categories[0] and ((num_neighbors - 1) < self.max_branching_factor)) \
                    or (category == self.ranked_categories[0] and (num_neighbors < self.max_branching_factor)):
                        self.hierarchy.add_edge(category, self.ranked_categories[i])
                        category_to_level[self.ranked_categories[i]] = category_to_level[category] + 1
                        if category_to_level[self.ranked_categories[i]] > self.num_hierarchy_levels:
                            self.num_hierarchy_levels = category_to_level[self.ranked_categories[i]]
                        if category in leaf_categories:
                            leaf_categories.remove(category)
                        break
            categories_used.add(self.ranked_categories[i])
            leaf_categories.add(self.ranked_categories[i])
        # Print the categories at each level in the hierarchy
        level_to_categories = {}
        for category in category_to_level:
            if category_to_level[category] not in level_to_categories:
                level_to_categories[category_to_level[category]] = []
            level_to_categories[category_to_level[category]].append(category)
        for level in level_to_categories:
            print("Level " + str(level) + ": " + str(level_to_categories[level]))
        # Determine paths to each leaf category
        paths_to_leaf_categories = []
        for category in leaf_categories:
            path = nx.shortest_path(self.hierarchy, source=self.ranked_categories[0],
                                    target=category)
            paths_to_leaf_categories.append(path)
        self.num_hierarchy_levels += 1
        # Assign wikia pages as leaves in the hierarchy
        for node in self.G.nodes():
            if len(node.categories) > 0:
                max_category_count = 0 #the most number of categories in common with the node
                max_category_path = [] #the path that has the most number of categories in common with the node
                for path in paths_to_leaf_categories:
                    current_category_count = 0
                    for category in path:
                        if category in node.categories:
                            current_category_count += 1
                    if current_category_count > max_category_count:
                        max_category_count = current_category_count
                        max_category_path = path
                self.hierarchy.add_node(node)
                self.hierarchy.add_edge(max_category_path[len(max_category_path) - 1], node)




