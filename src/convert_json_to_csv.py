import csv
import json
import os

def get_json(path):
    with open(os.path.join(path, 'node_removal.json')) as json_data:
        d = json.load(json_data)
        return d

def writeout(path):
    with open(os.path.join(path, 'node_removal.csv'), 'w') as csvfile:
        fieldnames = ['removed', 'numNodes', 'numEdges', 'averageInDegree', 'averageOutDegree', 'selfLinks', 'averagePathLength', 'sizeLargest']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        dataToWrite = get_json(path)
        for i in range(len(dataToWrite.keys())):
            writer.writerow(dataToWrite[str(i)])

def convert_dataset(path):
    dirs = os.listdir( path )
    for dir in dirs:
        try:
            writeout(dir)
            print("Finished " + dir)
        except:
            print("Nah " + dir)
    
