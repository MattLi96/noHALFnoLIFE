import networkx as nx
import numpy as np


class CategoryBasedHierarchicalModel:
    def __init__(self, G):
        """
        Initializations for a hierarchical model based on categories of the wikia pages
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
        self.category_similarity_matrix = self.get_category_similarity_matrix_by_co_occurrence()
        self.hierarchy = None

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

    def get_category_similarity_matrix_by_co_occurrence(self):
        """
        Builds a category similarity matrix based on co-occurrence of catgories, where the (i,j) entry is the count of
        co-occurence between the ith category and the jth category
        """
        similarity_matrix_counts = np.zeros((len(self.categories), len(self.categories)), dtype=np.int)
        for node in self.G.nodes():
            for i in range(len(node.categories)):
                for j in range(i + 1, len(node.categories)):
                    similarity_matrix_counts[i][j] += 1
                    similarity_matrix_counts[j][i] += 1
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
            # Find most similar node in hierarchy (according to the category similarity matrix) and add the current node
            # as a child of that node
            sorted_similarity_indices = np.argsort(self.category_similarity_matrix[i])[::-1]
            similar_categories = []
            for index in sorted_similarity_indices:
                similar_categories.append(self.index_to_category[index])
            for category in similar_categories:
                if category in categories_used:
                    self.hierarchy.add_edge(category, self.ranked_categories[i])
                    category_to_level[self.ranked_categories[i]] = category_to_level[category] + 1
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
        # Assign wikia pages as leaves in the hierarchy
        for node in self.G.nodes():
            paths_to_leaf_categories = []
            for category in leaf_categories:
                path = nx.shortest_path(self.hierarchy, source=self.ranked_categories[0],
                                                         target=category)
                paths_to_leaf_categories.append(path)
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




