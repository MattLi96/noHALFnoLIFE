#!/usr/bin/env python3
import sys
import xmltodict
import json


class XMLParser:
    def __init__(self, fname):
        self.file_name = fname
        pass

    def parse_to_obj(self, xml_attribs=True):
        print(self.file_name)
        with open(self.file_name, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs)
            return d

    def should_keep(self, node_title):
        IGNORE_LIST = ['Talk:', 'User:', 'File:', 'Thread:', 'Category:', 'Board Thread:', 'Template:', 'Category talk:', 'MediaWiki:', 'User blog comment:', 'Message Wall:', 'User blog:', 'Forum:', 'Board:']
        for item in IGNORE_LIST:
            if node_title[0:len(item)] == item:
                return False
            
        return True


if __name__ == '__main__':
    files = sys.argv
    files.pop(0)
    if len(files) < 0:
        files = get_data_files()["current"]

    for item in files:
        data_return = {}
        print(" --- Analyzing " + item + " ---")
        file_name = item
        parser = XMLParser(file_name)
        obj = parser.parse_to_obj()

        for p in obj["mediawiki"]["page"]:
            if not 'revision' in p:
                continue
            if not 'text' in p['revision']:
                continue
            if not '#text' in p['revision']['text']:
                continue
            name = p['title']
            if not parser.should_keep(name):
                continue
            text = p['revision']['text']['#text']

            data_return[name] = text

        data_output = json.dumps(data_return, indent=4, separators=(',', ':'))
        open(item[0:len(item) - 4] + '_dict.xml', 'w').write(data_output)
