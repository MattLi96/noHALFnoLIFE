import json
import os
import random

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import AdaBoostRegressor

from sklearn import linear_model
from sklearn import metrics

import matplotlib.pyplot as plt

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
    maxMins = [(0, 95), (200, 4000), (2, 22), (2, 7), (1000, 100000), (13, 22)]
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
                            yres= gpr.predict(testPt)
                            k = str(testPt)

                            if np.asscalar(yres) < minY[1]:
                                minY = (k, np.asscalar(yres))

                            ret[k] = {
                                "pred": np.asscalar(yres)
                            }
                            values[5] += float(maxMins[5][0]+maxMins[5][1])/n_steps
                        values[4] += float(maxMins[4][0]+maxMins[4][1])/n_steps
                    values[3] += float(maxMins[5][0]+maxMins[3][1])/n_steps
                values[2] += float(maxMins[2][0]+maxMins[2][1])/n_steps
            values[1] += float(maxMins[1][0]+maxMins[1][1])/n_steps
        values[0] += float(maxMins[0][0]+maxMins[0][1])/n_steps

    return ret, minY

def linearReg(x_train, y_train, x_test, y_test):
    # LINEAR ATTEMPT
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x_train, y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((regr.predict(x_test) - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(x_test, y_test))

    print("Predictions: ", regr.predict(x_test))
    print("Actual: ", y_test)

    return regr

def gpr(x_train, y_train, x_test, y_test):
    gpr = GaussianProcessRegressor(kernel=None, normalize_y =True)
    gpr.fit(x_train, y_train)

    print("Predicted: ", gpr.predict(x_test))
    print("Actual: ", y_test)

    print("Score on Test: ", gpr.score(x_test, y_test))
    print("Score on Validation: ", gpr.score(x_val, y_val))

    return gpr

def knn(x_train, y_train, x_test, y_test):
    knn = KNeighborsRegressor(3, 'distance', algorithm='auto')
    knn.fit(x_train, y_train)

    print("Predictions: ", knn.predict(x_test))
    print("Actual: ", y_test)

    return knn

def jiggle(x_train, y_train, epsilon):
    n, d = x_train.shape

    new_x = np.zeros((3*n, d))
    new_y = np.zeros(3*n)

    for i in range(0, n):
        new_x[i] = x_train[i]
        new_y[i] = y_train[i]

    for i in range(n, 3*n, 2):
        dim = random.randint(0, d-1)
        cop = random.randint(0, n-1)

        toadd = np.zeros(d)
        toadd[dim] += epsilon

        new_x[i] = x_train[cop] + toadd
        new_y[i] = y_train[cop]

        new_x[i+1] = x_train[cop] - toadd
        new_y[i+1] = y_train[cop]


    return new_x, new_y

def BOOSTING(x_train, y_train, x_test, y_test):
    rng = np.random.RandomState(1)
    regr = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),
                          n_estimators=3000, random_state=rng)
    # Train the model using the training sets
    regr.fit(x_train, y_train)
    print("Predictions: ", regr.predict(x_test))
    print("Actual: ", y_test)

    return regr

if __name__ == '__main__':
    path_reg = True

    listed_data = retrieve_basic_dicts("../data/")
    x, distributed_path_lengths, num_paths_found = convert_json_to_numpy(listed_data)

    # Splitting data
    y = distributed_path_lengths if path_reg else num_paths_found
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    x_test, x_val, y_test, y_val = train_test_split(x_test, y_test, test_size=0.5)

    # jiggled_x, jiggled_y = jiggle(x_train, y_train, 10)
    # print(x_train.shape)
    # print(jiggled_x.shape)

    # knn(x_train, y_train, x_test, y_test)

    # print("jiggle")
    # knn(jiggled_x, jiggled_y, x_test, y_test)

    regr = BOOSTING(x_train, y_train, x_test, y_test)
    grid, minY = grid_search(regr, 2)
    print(minY)
    with open('./grid_dump.json', 'w') as outfile:
        json.dump(grid, outfile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Logistic regression
    # regModel = LogisticRegression()
    # regModel.fit(x_train, y_train)
    # print("Score on Validation: ", regModel.score(x_train, y_train))

    # predicted = model2.predict(x_test)
    # print("Predicted: ", predicted)
    # print("Actual: ", y_test)

    # probs = model2.predict_proba(x_test)

    # print(metrics.accuracy_score(y_test, predicted))
    # print(metrics.roc_auc_score(y_test, probs[:, 1]))

    # grid, minY = grid_search(gpr, 2)

    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(minY)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # with open('./grid_dump.json', 'w') as outfile:
    #     json.dump(grid, outfile)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~