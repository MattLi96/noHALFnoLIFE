#!/usr/bin/env python3

import datetime as dt
import logging
import os
import sys
from logging.config import fileConfig
from multiprocessing import Pool

from network_analysis import NetworkAnalysis
from network_parser import NetworkParser
from xml_parser import XMLParser
from hierarchical_models import CategoryBasedHierarchicalModel

SNAPSHOT_TIME = "2015-12-05T02:20:10Z"
ONE_YEAR = 365
ONE_MONTH = 30


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


def process_file(data_file):
    # Parse Into Network
    d = XMLParser(data_file, get_time()).parse_to_dict()
    net = NetworkParser(d)

    # Graph Analysis
    output("Analyzing File: " + data_file)
    na = NetworkAnalysis(net.G, os.path.basename(data_file))
    na.outputBasicStats()
    na.outputNodesAndEdges()

    # Build Hierarchical Models
    if build_hierarchical_models:
        category_hierarchy = CategoryBasedHierarchicalModel(net.G)
        category_hierarchy.build_hierarchical_model()
    # na.generateDrawing()
    # generateComponentSizes doesn't work for directed graphs
    # na.generateComponentSizes()
    if len(sys.argv) > 1:
        na.d3dump("./public/data/")
    else:
        na.d3dump()
    output("Completed Analyzing: " + data_file)


# Main method
if __name__ == '__main__':
    FROM_NODE = len(sys.argv) > 1

    if FROM_NODE:
        output = lambda x: print(x)
    else:
        fileConfig('logging_config.ini')
        logger = logging.getLogger()
        output = lambda x: logger.debug(x)

    output("FROM_NODE: " + str(FROM_NODE))

    # Flags for control
    currentOnly = False
    noGame = True  # Only use the no game no life wiki. Intended for testing
    threads = 8  # Number of processes to use
    build_hierarchical_models = True

    # Setting datafiles to the correct files
    data_files = set()
    parseSet = get_data_files("./dataRaw").items() if len(sys.argv) > 1 else get_data_files().items()
    for (k, v) in parseSet:
        if not currentOnly:
            data_files.update(v)
        elif k == 'current':
            data_files.update(v)
    if noGame:
        data_files = {f for f in data_files if "nogamenolife" in f}

    # Processing the data_files
    with Pool(threads) as p:
        p.map(process_file, data_files)
