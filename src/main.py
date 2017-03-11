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
    pass

