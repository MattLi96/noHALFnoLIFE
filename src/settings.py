import os

category_hierarchical_model_settings = {
    "similarity_matrix_type": "cooccurrence",
    "max_branching_factor_root": 1  # specifies the root for the max branching factor function (max branching factor
    # calculated as kth root of number of page nodes (leaf nodes) in the hierarchy)
}
decentralized_search_settings = {
    "run_decentralized_search": False,
    "detailed_print": False,
    "hierarchy_nodes_only": True,
    "widen_search": '2look',  # possible values are 'none', '2look', 'hierarchy'
    "apply_weighted_score": True,
    "plots": True,
}

output_path = "../output/"
public_data = "../data/overview/"
public_out_path = "../public/data/"

current_only = True  # Only use current files. Has no effect in time series mode
no_game = True  # Only use the no game no life wiki. Intended for testing
no_game_name = "nogamenolife"
time_series = True  # If true do time series. Otherwise process file

generate_data = False  # True to generate data folder items

performance_mode = True
large_wikis = ["fullhouse", "gameofthrones", "marvel"]

cpu = os.cpu_count() if os.cpu_count() else 4
threads = cpu  # Adjust depending on how CPU/RAM intensive task is

path_length_cap = 200
