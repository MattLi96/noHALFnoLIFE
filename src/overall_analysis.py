import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
import os
import json

def retrieve_basic_dicts(dir, current_only=True):
	files = os.listdir(dir)
	only_current = list(filter(lambda x: "current" in x, files))

	list_to_analyze = only_current if current_only else files
	
	ret = []

	for f in list_to_analyze:
		full_path = os.path.join(dir, f)
		with open(full_path) as json_data:
		    d = json.load(json_data)
		    ret.append(d['basic'])

	return ret

def convert_json_to_numpy(li):
	# Dimensions of the Matrix
 	n,d = len(li), len(li[0].values())-1
 	x = np.zeros((n,d))
 	distributed_path_len = np.zeros(n)
 	num_paths_found = np.zeros(n)

 	order = ["selfLinks", "numNodes", "averageInDegree", "averagePathLength", "numEdges", "averageOutDegree"]

 	assert d==len(order)
 	
 	for idx, item in enumerate(li):
 		distributed_path_len[idx] = item["decentralized"]["average_decentralized_path_length"]
 		num_paths_found[idx] = item["decentralized"]["num_paths_found"]
 		for i in range(d):
 			x[idx][i] = float(item[order[i]])

 	return x, distributed_path_len, num_paths_found

if __name__ == '__main__':
	listed_data = retrieve_basic_dicts("../public/data/")
	x, distributed_path_lengths, num_paths_found = convert_json_to_numpy(listed_data)