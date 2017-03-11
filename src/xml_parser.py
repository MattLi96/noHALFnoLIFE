#!/usr/bin/env python3
import sys
import xmltodict
import json
import datetime


class XMLParser:
    def __init__(self, fname, snapshot_time=None):
        self.file_name = fname
        self.time = snapshot_time
        pass

    def parse_to_obj(self, xml_attribs=True):
        print("analyzing file: " + self.file_name)
        with open(self.file_name, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs)
            return d

    def should_keep(self, node_title):
        IGNORE_LIST = ['Talk:', 'User:', 'File:', 'Thread:', 'Category:', 'Board Thread:', 'Template:', 'Category talk:', 'MediaWiki:', 'User blog comment:', 'Message Wall:', 'User blog:', 'Forum:', 'Board:']
        for item in IGNORE_LIST:
            if node_title[0:len(item)] == item:
                return False
            
        return True

    def parse_to_dict(self):
        data_return = {}
        obj = self.parse_to_obj()
        for p in obj["mediawiki"]["page"]:
            if not 'revision' in p:
                continue
            if not 'text' in p['revision']:
                for item in p['revision']:
                    time = item['timestamp']
                    #format is 2014-12-17T02:25:15Z
                    time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                continue
            if not '#text' in p['revision']['text']:
                continue
            name = p['title']
            if not self.should_keep(name):
                continue
            text = p['revision']['text']['#text']

            data_return[name] = text

        return data_return

