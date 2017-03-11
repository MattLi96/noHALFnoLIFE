from xml_parser import XMLParser
from network_parser import NetworkParser
from network_analysis import NetworkAnalysis

from os import listdir
from os.path import isfile, join


def get_data_files(dir_path="../data"):
    ret = {"current": set(), "full": set()}
    for f in listdir(dir_path):
        rel_path = join(dir_path, f)
        if isfile(rel_path):
            if f.endswith("_current.xml"):
                ret['current'].add(rel_path)
            elif f.endswith("_full.xml"):
                ret['full'].add(rel_path)
    return ret


if __name__ == '__main__':
    # Flags for control
    currentOnly = True
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
        net = NetworkParser.createGraphFromDict(d)
        networks[f] = net

    for (k, v) in networks.items():
        NetworkAnalysis(v, k)
