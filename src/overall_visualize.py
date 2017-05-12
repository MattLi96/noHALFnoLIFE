#!/usr/bin/env python3
import json
import os
import shutil

import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = "../data/capped/none_unweighted/overview/"
OUTPUT_PATH = "../output/visual/"

FIELDS = {0: 'numNodes',
          1: 'numEdges',
          2: 'averageInDegree',
          3: 'averageOutDegree',
          4: 'selfLinks',
          5: 'averagePathLength',
          6: 'decentralized_num_paths_found',
          7: 'decentralized_num_paths_missing',
          8: 'decentralized_average_decentralized_path_length',
          9: 'decentralized_average_num_unique_nodes',
          10: 'hierarchy_num_nodes',
          11: 'hierarchy_num_levels',
          12: 'path_length_10_percentile',
          13: 'path_length_20_percentile',
          14: 'path_length_30_percentile',
          15: 'path_length_40_percentile',
          16: 'path_length_50_percentile',
          17: 'path_length_60_percentile',
          18: 'path_length_70_percentile',
          19: 'path_length_80_percentile',
          20: 'path_length_90_percentile',
          21: 'random_num_paths_found',
          22: 'random_num_paths_missing',
          23: 'random_average_decentralized_path_length',
          24: 'random_average_num_unique_nodes'}

TITLEDICT = {'numNodes': 'Number of Nodes',
             'numEdges': 'Number of Edges',
             'averageInDegree': 'Average Indegree',
             'averageOutDegree': 'Average Outdegree',
             'selfLinks': 'Number of Self-links',
             'averagePathLength': 'Average Path Length',
             'decentralized_num_paths_found': 'Number of Paths Found with Decentralized Search',
             'decentralized_num_paths_missing': 'Number of Paths Missing from Decentralized Search',
             'decentralized_average_decentralized_path_length': 'Average Decentralized Search Path Length',
             'decentralized_average_num_unique_nodes': 'Average Number of Unique Nodes in Decentralized Search Paths',
             'hierarchy_num_nodes': 'Number of Nodes in Hierarchy',
             'hierarchy_num_levels': 'Number of Levels in Hierarchy',
             'path_length_10_percentile': 'Path Length (10th percentile)',
             'path_length_20_percentile': 'Path Length (20th percentile)',
             'path_length_30_percentile': 'Path Length (30th percentile)',
             'path_length_40_percentile': 'Path Length (40th percentile)',
             'path_length_50_percentile': 'Path Length (50th percentile)',
             'path_length_60_percentile': 'Path Length (60th percentile)',
             'path_length_70_percentile': 'Path Length (70th percentile)',
             'path_length_80_percentile': 'Path Length (80th percentile)',
             'path_length_90_percentile': 'Path Length (90th percentile)',
             'random_num_paths_found': 'Number of Paths Found with Random Search',
             'random_num_paths_missing': 'Number of Paths Missing from Random Search',
             'random_average_decentralized_path_length': 'Average Random Search Path Length',
             'random_average_num_unique_nodes': 'Average Number of Unique Nodes in Random Search Paths'}


def get_title(key):
    return TITLEDICT[key]


def retrieve_basic_dicts(dir):
    files = os.listdir(dir)
    ret = []
    for f in files:
        full_path = os.path.join(dir, f)
        with open(full_path) as json_data:
            d = json.load(json_data)
            d["file"] = os.path.splitext(f)[0].split("_")[0]
            ret.append(d)
    return ret


def compare_hiearchy_random():
    out_path = OUTPUT_PATH + "compare.png"

    fig, ax = plt.subplots()
    plt.title("Average Path Length")

    plt.xlabel("Random")
    plt.ylabel("Hierarchy")

    plot_compare_hiearchy_random("../data/capped/none_unweighted/overview/", 'r', "Baseline")
    plot_compare_hiearchy_random("../data/capped/none_weighted/overview/", 'y', "Weighted")
    # plot_compare_hiearchy_random("../data/capped/2look_unweighted/overview/", 'g', "Lookahead")
    # plot_compare_hiearchy_random("../data/capped/hierarchy_unweighted/overview/", 'm', "Hierarchy")
    # plot_compare_hiearchy_random("../data/capped/2look_weighted/overview/", 'c', "Weighted Lookahead")
    # plot_compare_hiearchy_random("../data/capped/both_2look/overview/", 'm', "Lookahead")

    # Line
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]
    ax.plot(lims, lims, 'k-')

    plt.legend(loc=4)

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(out_path)
    plt.close()


def plot_compare_hiearchy_random(data_path, color, label, point_labels=False):
    data = retrieve_basic_dicts(data_path)
    xdata = list(map(lambda z: z[FIELDS[23]], data))  # Random
    ydata = list(map(lambda z: z[FIELDS[8]], data))  # Hierarchy
    plt.scatter(x=xdata, y=ydata, c=color, label=label)
    if point_labels:
        pls = list(map(lambda z: z["file"], data))
        for l, x, y in zip(pls, xdata, ydata):
            plt.annotate(l, xy=(x, y))


def visualize(data):
    xfields = [i for _, i in FIELDS.items()]
    xdata = {}
    for x in xfields:
        data = list(filter(lambda z: x in z, data))
    for x in xfields:
        xdata[x] = list(map(lambda z: z[x], data))

    decentralized_fields = [FIELDS[16], FIELDS[8], FIELDS[9], FIELDS[6]]
    ydata = {}
    for y in decentralized_fields:
        ydata[y] = list(map(lambda z: z[y], data))

    for x, xd in xdata.items():
        for y, yd in ydata.items():
            makePlot('{} to {}'.format(get_title(x), get_title(y)), get_title(x), get_title(y), xd, yd,
                '{}_{}.png'.format(y, x))


def makePlot(title, xaxis, yaxis, xdata, ydata, out):
    out_path = OUTPUT_PATH + out
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')

    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

    plt.scatter(x=xdata, y=ydata)

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(out_path)
    plt.close()


if __name__ == '__main__':
    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)

    # compare_hiearchy_random()
    visualize(retrieve_basic_dicts(DATA_PATH))
