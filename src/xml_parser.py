#!/usr/bin/env python3
from datetime import datetime

import xmltodict


class XMLParser:
    def __init__(self, fname, snapshot_time=datetime.now()):
        self.file_name = fname
        self.time = snapshot_time
        pass

    def parse_to_obj(self, xml_attribs=True):
        print("Parsing File: " + self.file_name)
        with open(self.file_name, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs)
            return d

    def should_keep(self, node_title):
        IGNORE_LIST_PREFIX = ['Talk:', 'User:', 'File:', 'Thread:', 'Category:', 'Board Thread:', 'Template:',
                              'Category talk:', 'MediaWiki:', 'User blog comment:', 'Message Wall:', 'User blog:',
                              'Forum:', 'Board:', 'Help:', 'User talk:', 'Blog:', 'Top 10 list:']
        IGNORE_LIST_SUFFIX = [':Templates', ':Copyrights', ':Candidates for speedy deletion', ':Privacy policy',
                              ':Administrators', ':Navigation', ':Bureaucrats', ':Community Portal',
                              ':Terminology List', ':Sandbox', ':Welcome', ':Policy', ':Protected page',
                              '/Unofficial chat', ':About']

        for item in IGNORE_LIST_PREFIX:
            if node_title[0:len(item)] == item:
                return False

        for item in IGNORE_LIST_SUFFIX:
            if node_title[len(node_title) - len(item): len(node_title)] == item:
                return False

        return True

    def parse_to_dict(self):
        data_return = {}
        obj = self.parse_to_obj()
        for p in obj["mediawiki"]["page"]:
            if not 'revision' in p:
                continue
            rev = p['revision']
            if not 'text' in rev:
                latest_text = None
                latest_time = None
                for item in rev:
                    time = item['timestamp']
                    # format is 2014-12-17T02:25:15Z
                    time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                    if latest_time:
                        if (time_obj > latest_time and time_obj < self.time):
                            latest_time = time_obj
                            latest_text = item['text']
                    elif time_obj <= self.time:
                        latest_time = time_obj
                        latest_text = item['text']
                text_obj = latest_text
            else:
                text_obj = rev['text']
            if not '#text' in text_obj:
                continue
            name = p['title']
            if not self.should_keep(name):
                continue
            text = text_obj['#text']

            data_return[name] = text

        return data_return
