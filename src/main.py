#!/usr/bin/env python3
from xml_parser import XMLParser
from network_parser import NetworkParser
from network_analysis import NetworkAnalysis
import os
from os import listdir
from os.path import isfile, join
import json

def get_data_files(dir_path="../data"):
    ret = {"current": set(), "full": set()}
    for f in os.listdir(dir_path):
        rel_path = os.path.join(dir_path, f)
        if os.path.isfile(rel_path):
            if f.endswith("_current.xml"):
                ret['current'].add(rel_path)
            elif f.endswith("_full.xml"):
                ret['full'].add(rel_path)
    return ret


if __name__ == '__main__':
    # Flags for control
    currentOnly = False
    noGame = True  # Only use the no game no life wiki. Intended for testing

    # Setting datafiles to the correct files
    data_files = set()
    for (k, v) in get_data_files().items():
        if not currentOnly:
            data_files.update(v)
        elif k == 'current':
            data_files.update(v)
    if noGame:
        data_files = {f for f in data_files if "nogamenolife" in f}

    # Processing networks
    networks = {}
    for f in data_files:
        d = XMLParser(f).parse_to_dict()
        net = NetworkParser(d)
        networks[f] = net.G

        #TODO: Remove these outputs
        open(f[0:len(f) - 4] + '_dict.json', 'w').write(json.dumps(d,indent=4, separators=(',', ': ')))

    for (k, v) in networks.items():
        na = NetworkAnalysis(v, os.path.basename(k))
        na.outputBasicStats()
        na.generateDrawing()
        na.generateComponentSizes()
