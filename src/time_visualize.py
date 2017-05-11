#!/usr/bin/env python3
import json
import os
import shutil

import matplotlib.pyplot as plt
import matplotlib.colors as col
from matplotlib.dates import date2num
import datetime as dt
import numpy as np

DATA_PATH = "../data/jared/none_weighted_time/overview/"
OUTPUT_PATH = "../output/visual/jared_time_weighted/"

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

TITLEDICT = { 'numNodes': 'Number of Nodes',
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




def retrieve_basic_dicts(dir):
    files = os.listdir(dir)
    ret = []
    dates = []
    filearr = []
    for f in files:
        last_tag = f.split('.')[-2].split('_')[-1]
        if last_tag == 'current':
            continue
        this_date = dt.datetime.strptime(last_tag, '%Y-%m-%d')
        filearr.append((this_date, f))
    filearr = sorted(filearr, key = lambda x: x[0])
    for f in filearr:
        full_path = os.path.join(dir, f[1])
        with open(full_path) as json_data:
            d = json.load(json_data)
            ret.append(d)
            dates.append(f[0])
    return (ret, dates)

def get_title(key):
    return TITLEDICT[key]

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
    (data, dates) = retrieve_basic_dicts(data_path)
    xdata = list(map(lambda z: z[FIELDS[24]], data))  # Random
    ydata = list(map(lambda z: z[FIELDS[9]], data))  # Hierarchy
    plt.scatter(x=xdata, y=ydata, c=color, label=label)


def visualize(data, dates=None):
    xfields = [i for _, i in FIELDS.items()]
    xdata = {}
    for x in xfields:
        data = list(filter(lambda z: x in z, data))
    for x in xfields:
        xdata[x] = list(map(lambda z: z[x], data))

    #decentralized_fields = [FIELDS[16], FIELDS[6], FIELDS[8], FIELDS[9]]
    decentralized_fields = FIELDS.values()
    agesteps = dates if dates else range(0, len(xdata[FIELDS[0]]))
    agesteps.pop(0)

    ydata = {}
    for y in decentralized_fields:
        ydata[y] = list(map(lambda z: z[y], data))

    for y, yd in ydata.items():
        makePlot('{} to {}'.format('Time', get_title(y)), 'Time', get_title(y), agesteps, yd, '{}_{}.png'.format('Time', get_title(y)))
        #for x, xd in xdata.items():
        #    makePlot('{} to {}'.format(get_title(x), get_title(y)), get_title(x), get_title(y), xd, yd, '{}_{}.png'.format(get_title(y), get_title(x)))

def getColArray(arrlength, col1 = [0.3, 0.6, 0.3, 0.2], col2 = [0.3, 0.6, 0.3, 1]):
    a = []
    for i in range (0, arrlength):
        newarr = []
        for j in range(0, len(col1)):
            newarr.append((col1[j] * (arrlength - i)/arrlength) + (col2[j] * i/arrlength))
        a.append(newarr)
    return a

def makePlot(title, xaxis, yaxis, xdata, ydata, out):
    out_path = OUTPUT_PATH + out
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.xticks(rotation=17, horizontalalignment='right')

    plt.xlabel(xaxis)
    plt.ylabel(yaxis)

    plt.scatter(x=xdata, y=ydata, c=getColArray(len(xdata)))

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
    visualize(*retrieve_basic_dicts(DATA_PATH))
