#!/usr/bin/env python3
import sys
import xmltodict
import json
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


class XMLParser:
    def __init__(self, fname):
        self.file_name = fname
        pass

    def filter(self):
        pass

    def parse_to_obj(self, xml_attribs=True):
        print(self.file_name)
        with open(self.file_name, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs)
            return d

    def parse_to_dict(self):
        d = self.parse_to_obj()


if __name__ == '__main__':
    files = sys.argv
    files.pop(0)
    if len(files) < 0:
        print("No file specified. Specify at least one file")
        exit(0)

    for item in files:
        data_return = {}
        print(" --- Analyzing " + item + " ---")
        file_name = item
        obj = XMLParser(file_name).parse_to_obj()

        for p in obj["mediawiki"]["page"]:
            name = None
            text = None
            for dict_item in p:
                if (dict_item[0] == "title"):
                    name = dict_item[1]
                elif (dict_item[0] == "#text"):
                    text = dict_item[1]
                if (name and text):
                    break
            data_return[name] = text

        data_output = json.dumps(data_return)
        open(item[0:len(item) - 4] + '_dict.xml', 'w').write(data_output)
