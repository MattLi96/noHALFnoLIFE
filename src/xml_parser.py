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

    def parse_to_dict(file_name):
        data_return = {}
        obj = self.parse_to_obj()
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

        return data_return

