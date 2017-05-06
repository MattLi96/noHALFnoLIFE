import json
import os

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor

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


def convert_json_to_numpy(li):
    # Dimensions of the Matrix
    n, d = len(li), len(li[0].values()) - 1
    x = np.zeros((n, d))
    distributed_path_len = np.zeros(n)
    num_paths_found = np.zeros(n)

    order = ["selfLinks", "numNodes", "averageInDegree", "averagePathLength", "numEdges", "averageOutDegree"]

    assert d == len(order)

    for idx, item in enumerate(li):
        distributed_path_len[idx] = item["decentralized"]["average_decentralized_path_length"]
        num_paths_found[idx] = item["decentralized"]["num_paths_found"]
        for i in range(d):
            x[idx][i] = float(item[order[i]])

    return x, distributed_path_len, num_paths_found


def grid_search(gpr, n_steps):
    maxMins = [(0, 20), (100, 10000), (1, 10), (1, 10), (100, 20000), (1, 10)]
    values = list(map(lambda x: x[0], maxMins))

    ret = {}
    minY = ("", 9999)

    while values[0] <= maxMins[0][1]:
        values[1] = maxMins[1][0]
        while values[1] <= maxMins[1][1]:
            values[2] = maxMins[2][0]
            while values[2] <= maxMins[2][1]:
                values[3] = maxMins[3][0]
                while values[3] <= maxMins[3][1]:
                    values[4] = maxMins[4][0]
                    while values[4] <= maxMins[4][1]:
                        values[5] = maxMins[5][0]
                        while values[5] <= maxMins[5][1]:
                            testPt = np.array(values)
                            yres, sig= gpr.predict(testPt, return_std=True)
                            k = str(testPt)

                            if np.asscalar(yres) < minY[1]:
                                minY = (k, np.asscalar(yres))

                            ret[k] = {
                                "pred": np.asscalar(yres),
                                "deviation": np.asscalar(sig)
                            }
                            values[5] += float(maxMins[5][0]+maxMins[5][1])/n_steps
                        values[4] += float(maxMins[4][0]+maxMins[4][1])/n_steps
                    values[3] += float(maxMins[5][0]+maxMins[3][1])/n_steps
                values[2] += float(maxMins[2][0]+maxMins[2][1])/n_steps
            values[1] += float(maxMins[1][0]+maxMins[1][1])/n_steps
        values[0] += float(maxMins[0][0]+maxMins[0][1])/n_steps

    return ret, minY

if __name__ == '__main__':
    path_reg = True

    listed_data = retrieve_basic_dicts("../data/")
    x, distributed_path_lengths, num_paths_found = convert_json_to_numpy(listed_data)

    # Splitting data
    y = distributed_path_lengths if path_reg else num_paths_found
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5)

    gpr = GaussianProcessRegressor(kernel=None, normalize_y =True)
    gpr.fit(x_train, y_train)
    print("Score on Validation: ", gpr.score(x_val, y_val))
    # print(gpr.predict([1, 1170, 6.4, 2.7, 1200, 6.4]))
    
    grid, minY = grid_search(gpr, 2)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(minY)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    with open('./grid_dump.json', 'w') as outfile:
        json.dump(grid, outfile)
