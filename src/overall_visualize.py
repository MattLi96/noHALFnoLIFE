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


def retrieve_basic_dicts(dir, current_only=True):
    files = os.listdir(dir)
    only_current = list(filter(lambda x: "current" in x, files))

    list_to_analyze = only_current if current_only else files

    ret = []
    for f in list_to_analyze:
        full_path = os.path.join(dir, f)
        with open(full_path) as json_data:
            d = json.load(json_data)
            ret.append(d)
    return ret


def compare_hiearchy_random():
    out_path = OUTPUT_PATH + "compare.png"

    fig, ax = plt.subplots()
    plt.title("Random To Hierarchy Unique Nodes")

    plt.xlabel("Random")
    plt.ylabel("Hierarchy")

    plot_compare_hiearchy_random("../data/capped/none_unweighted/overview/", 'r', "Baseline")
    plot_compare_hiearchy_random("../data/capped/none_weighted/overview/", 'b', "Weighted")
    plot_compare_hiearchy_random("../data/capped/2look_unweighted/overview/", 'g', "Lookahead")

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


def plot_compare_hiearchy_random(data_path, color, label):
    data = retrieve_basic_dicts(data_path)
    xdata = list(map(lambda z: z[FIELDS[24]], data))  # Random
    ydata = list(map(lambda z: z[FIELDS[9]], data))  # Hierarchy
    plt.scatter(x=xdata, y=ydata, c=color, label=label)


def visualize(data):
    xfields = [i for _, i in FIELDS.items()]
    xdata = {}
    for x in xfields:
        xdata[x] = list(map(lambda z: z[x], data))

    decentralized_fields = [FIELDS[16], FIELDS[6], FIELDS[8], FIELDS[9]]
    ydata = {}
    for y in decentralized_fields:
        ydata[y] = list(map(lambda z: z[y], data))

    for x, xd in xdata.items():
        for y, yd in ydata.items():
            makePlot('{} to {}'.format(x, y), x, y, xd, yd, '{}_{}.png'.format(y, x))


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

    compare_hiearchy_random()
    visualize(retrieve_basic_dicts(DATA_PATH))
