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
        Builds a category similarity matrix based on co-occurrence of tags, where a row is a list of all categories
        ordered from most to least similar
        """
        similarity_matrix_counts = np.zeros((len(self.categories), len(self.categories)), dtype=np.int)
        for node in self.G.nodes():
            for i in range(len(node.categories)):
                for j in range(i + 1, len(node.categories)):
                    similarity_matrix_counts[i][j] += 1
                    similarity_matrix_counts[j][i] += 1
        similarity_matrix = np.empty((len(self.categories), len(self.categories)), dtype='object')
        for k in range(len(similarity_matrix)):
            sorted_similarity_indices = np.argsort(similarity_matrix_counts[k])[::-1]
            row_categories_order = []
            for index in sorted_similarity_indices:
                row_categories_order.append(self.index_to_category[index])
            similarity_matrix[k] = row_categories_order
        return similarity_matrix

    def build_hierarchical_model(self):
        """
        Builds a hierarchical model that can be used for decentralized search by using the ranked categories list (based
        on a centrality of the measure) and the category similarity matrix
        """
        self.hierarchy = nx.Graph()
        categories_used = set()
        category_to_level = {}
        self.hierarchy.add_node(self.ranked_categories[0])
        category_to_level[self.ranked_categories[0]] = 0
        categories_used.add(self.ranked_categories[0])
        for i in range(1, len(self.ranked_categories)):
            self.hierarchy.add_node(self.ranked_categories[i])
            # Find most similar node in hierarchy (according to the category similarity matrix) and add the current node
            # as a child of that node
            for category in self.category_similarity_matrix[i]:
                if category in categories_used:
                    self.hierarchy.add_edge(category, self.ranked_categories[i])
                    category_to_level[self.ranked_categories[i]] = category_to_level[category] + 1
                    break
            categories_used.add(self.ranked_categories[i])
        # Print the nodes at each level in the hierarchy
        level_to_categories = {}
        for category in category_to_level:
            if category_to_level[category] not in level_to_categories:
                level_to_categories[category_to_level[category]] = []
            level_to_categories[category_to_level[category]].append(category)
        for level in level_to_categories:
            print("Level " + str(level) + ": " + str(level_to_categories[level]))
