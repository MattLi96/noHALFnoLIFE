#!/usr/bin/env python3
category_hierarchical_model_settings = {
    "similarity_matrix_type": "cooccurrence",
    "max_branching_factor_root": 1  # specifies the root for the max branching factor function (max branching factor
    # calculated as kth root of number of page nodes (leaf nodes) in the hierarchy)
}
decentralized_search_settings = {
    "run_decentralized_search": True,
    "detailed_print": False,
    "hierarchy_nodes_only": True,
    "widen_search": False,
    "apply_weighted_score": True,
    "plots": False
}
from_node = False
output_path = ""
current_only = True  # Only use current files. Has no effect in time series mode
no_game = True  # Only use the no game no life wiki. Intended for testing
no_game_name = "nogamenolife"
time_series = False  # If true do time series. Otherwise process file

threads = 16
