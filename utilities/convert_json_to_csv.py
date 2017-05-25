import csv
import json
import os

def get_json(path):
    """
    get_json finds the .nodeRemove object at the given path and returns the corresponding json object

    Args:
    path: the path location as a string

    Returns:
    The JSON object associated with the path
    """
    pathAttempt = os.path.join(path, 'nodeRemove.json')
    with open(pathAttempt, 'r') as json_data:
        return json.load(json_data)

def writeout(path):
    """
    writeout converts the nodeRemove JSON file into a CSV file within the same folder

    Args:
    path: the path location as a string
    """
    pathName = os.path.join(path, 'node_removal.csv')
    with open(pathName, 'w') as csvfile:
        fieldnames = ['removed', 'numNodes', 'numEdges', 'averageInDegree', 'averageOutDegree', 'selfLinks', 'averagePathLength', 'sizeLargest']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        dataToWrite = get_json(path)
        for i in range(len(dataToWrite.keys())):
            writer.writerow(dataToWrite[str(i)])

def convert_dataset(path):
    """
    convert_dataset converts all nodeRemove JSON files in the given folder into CSV files

    Args:
    path: the path location of the folder as a string
    """
    dirs = os.listdir( path )
    for dir in dirs:
        try:
            pathAttempt = os.path.join(path, dir)
            writeout(pathAttempt)
            print("Finished " + dir)
        except:
            print("Could not write " + dir)
    
convert_dataset("../data/full/none_unweighted")