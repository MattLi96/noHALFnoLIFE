import csv
import json
import os

def get_json(path):
    pathAttempt = os.path.join(path, 'nodeRemove.json')
    print("read from", pathAttempt)
    with open(pathAttempt, 'r') as json_data:
        print("got file")
        d = json.load(json_data)
        return d

def writeout(path):
    pathName = os.path.join(path, 'node_removal.csv')
    print(pathName)
    with open(pathName, 'w') as csvfile:
        print("writing")
        fieldnames = ['removed', 'numNodes', 'numEdges', 'averageInDegree', 'averageOutDegree', 'selfLinks', 'averagePathLength', 'sizeLargest']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        print("about to write header")
        writer.writeheader()
        
        print("getting data")
        dataToWrite = get_json(path)
        print("writing data")
        for i in range(len(dataToWrite.keys())):
            writer.writerow(dataToWrite[str(i)])

def convert_dataset(path):
    dirs = os.listdir( path )
    for dir in dirs:
        try:
            pathAttempt = os.path.join(path, dir)
            writeout(pathAttempt)
            print("Finished " + dir)
        except:
            print("Nah " + dir)
    
convert_dataset("../data/full/none_unweighted")