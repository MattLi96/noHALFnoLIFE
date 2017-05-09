import json
import os
import shutil

import matplotlib.pyplot as plt

DATA_PATH = "../data/"
OUTPUT_PATH = "../output/overall/"


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


def visualize(data):
    xfields = ["selfLinks", "numNodes", "averagePathLength", "numEdges", "averageOutDegree"]
    xdata = {}
    for x in xfields:
        xdata[x] = list(map(lambda z: z[x], data))

    decentralized_fields = ["average_num_unique_nodes", "average_decentralized_path_length", "num_paths_found"]
    ydata = {}
    for y in decentralized_fields:
        ydata[y] = list(map(lambda z: z['decentralized'][y], data))

    for x, xd in xdata.items():
        for y, yd in ydata.items():
            makePlot('{} to {}'.format(x, y), x, y, xd, yd, '{}_{}.png'.format(y, x))


def makePlot(title, xaxis, yaxis, xdata, ydata, out):
    out_path = OUTPUT_PATH + out
    fig = plt.figure()
    fig.suptitle(title, fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    ax.set_xlabel(xaxis)
    ax.set_ylabel(yaxis)

    ax.scatter(x=xdata, y=ydata)
    plt.scatter(x=xdata, y=ydata)

    directory = os.path.dirname(out_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    plt.savefig(out_path)
    plt.close()


if __name__ == '__main__':
    listed_data = retrieve_basic_dicts(DATA_PATH)

    if os.path.exists(OUTPUT_PATH):
        shutil.rmtree(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH)
    visualize(listed_data)
