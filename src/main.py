#!/usr/bin/env python3


import datetime as dt
import logging
import os
import shutil
import sys
from logging.config import fileConfig
from multiprocessing import Pool

from decentralized_search import HierarchicalDecentralizedSearch
from hierarchical_models import CategoryBasedHierarchicalModel
from network_analysis import NetworkAnalysis
from network_parser import NetworkParser
from settings import *
from xml_parser import XMLParser

SNAPSHOT_TIME = "2015-12-05T02:20:10Z"
OLDEST_TIME = dt.datetime(2000, 1, 1)
ONE_YEAR = 365
ONE_MONTH = 30
TIME_INCR = dt.timedelta(days=30)


def get_data_files(dir_path=None):
    if dir_path is None:
        dir_path = "../dataRaw"

    output("Getting files from " + dir_path)

    ret = {"current": set(), "full": set()}
    for f in os.listdir(dir_path):
        rel_path = os.path.join(dir_path, f)
        if os.path.isfile(rel_path):
            if f.endswith("_current.xml"):
                ret['current'].add(rel_path)
            elif f.endswith("_full.xml"):
                ret['full'].add(rel_path)
    output(str(len(ret["current"])) + " current files")
    output(str(len(ret["full"])) + " full files")
    return ret


def get_time():
    return dt.datetime.strptime(SNAPSHOT_TIME, '%Y-%m-%dT%H:%M:%SZ')


# basically a class so we can have a thread pool
class Runner:
    def __init__(self):
        self.threads = threads
        self.pool = Pool(threads)

    @staticmethod
    def process_file(data_file):
        curr_time = get_time()
        # Parse Into Network
        d = XMLParser(data_file, get_time()).parse_to_dict()
        net = NetworkParser(d)
        # Graph Analysis
        output("Analyzing File " + data_file)
        na = NetworkAnalysis(net.G, os.path.basename(data_file), output_path)
        na.outputBasicStats()
        na.outputNodesAndEdges()
        na.nodeRemoval()

        basic = na.d3dump("../public/data/", str(curr_time))

        # Run Decentralized Search
        if decentralized_search_settings["run_decentralized_search"]:
            category_hierarchy = CategoryBasedHierarchicalModel(net.G,
                similarity_matrix_type=category_hierarchical_model_settings["similarity_matrix_type"],
                max_branching_factor_root=category_hierarchical_model_settings["max_branching_factor_root"]
            )
            category_hierarchy.build_hierarchical_model()
            decentralized_search_model = HierarchicalDecentralizedSearch(net.G, category_hierarchy.hierarchy,
                detailed_print=decentralized_search_settings["detailed_print"],
                hierarchy_nodes_only=decentralized_search_settings["hierarchy_nodes_only"],
                apply_weighted_score=decentralized_search_settings["apply_weighted_score"],
            )
            n_found, n_missing, av_path_len, av_unique_nodes = decentralized_search_model.run_decentralized_search(1000,
                decentralized_search_settings["widen_search"], decentralized_search_settings["plots"])

            basic["decentralized"] = {
                "num_paths_found": n_found,
                "num_paths_missing": n_missing,
                "average_decentralized_path_length": av_path_len,
                "average_num_unique_nodes": av_unique_nodes
            }

        na.write_permanent_data_json("../data/", basic)

        # na.generateDrawing()
        # generateComponentSizes doesn't work for directed graphs
        # na.generateComponentSizes()

        output("Completed Analyzing: " + data_file)

    @staticmethod
    def time_process(data_file):
        curr_time = dt.datetime.now()
        # run loop
        fobj = XMLParser(data_file, curr_time)
        lim = fobj.find_oldest_time()
        while curr_time > lim:
            curr_time -= TIME_INCR
            print('running time analysis for ' + str(curr_time))
            fobj.update_time(curr_time)
            d = fobj.parse_to_dict()
            if d:
                net = NetworkParser(d)
                output("Analyzing File " + data_file + ' at time ' + str(curr_time))
                na = NetworkAnalysis(net.G, os.path.basename(data_file), output_path)
                na.d3dump("../public/data/", str(curr_time))

                # Run Decentralized Search
                if decentralized_search_settings["run_decentralized_search"]:
                    category_hierarchy = CategoryBasedHierarchicalModel(net.G,
                        similarity_matrix_type=category_hierarchical_model_settings["similarity_matrix_type"],
                        max_branching_factor_root=category_hierarchical_model_settings["max_branching_factor_root"]
                    )
                    category_hierarchy.build_hierarchical_model()
                    decentralized_search_model = HierarchicalDecentralizedSearch(net.G, category_hierarchy.hierarchy,
                        detailed_print=decentralized_search_settings["detailed_print"],
                        hierarchy_nodes_only=decentralized_search_settings["hierarchy_nodes_only"],
                        apply_weighted_score=decentralized_search_settings["apply_weighted_score"],
                    )
                    n_found, n_missing, av_path_len, av_unique_nodes = decentralized_search_model.run_decentralized_search(1000,
                        decentralized_search_settings["widen_search"], decentralized_search_settings["plots"])

                    basic["decentralized"] = {
                        "num_paths_found": n_found,
                        "num_paths_missing": n_missing,
                        "average_decentralized_path_length": av_path_len,
                        "average_num_unique_nodes": av_unique_nodes
                    }

                na.write_permanent_data_json("../data/", basic, tag=curr_time)

        output("Completed Analyzing: " + data_file)

    def main(self):
        # Setting datafiles to the correct files
        data_files = set()
        parse_set = get_data_files().items()
        for (k, v) in parse_set:
            if time_series:  # If doing a time series, only worth checking out full stuff
                if k == 'full':
                    data_files.update(v)
                else:
                    continue

            # Non-time series
            if not current_only:
                data_files.update(v)
            elif k == 'current':
                data_files.update(v)
        print(data_files)
        if no_game:
            data_files = {f for f in data_files if no_game_name in f}

        # Clear output
        if os.path.exists(output_path):
            shutil.rmtree(output_path)

        # Processing the data_files
        if time_series:
            self.pool.map(Runner.time_process, data_files)
        else:
            self.pool.map(Runner.process_file, data_files)

        self.pool.close()
        self.pool.join()


# Main method
if __name__ == '__main__':
    fileConfig('logging_config.ini')
    logger = logging.getLogger()
    output = lambda x: logger.debug(x)\

    output_path = "../output/"

    Runner().main()  # Runs the actual processing.
