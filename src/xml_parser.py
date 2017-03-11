import untangle
import sys


class XMLParser:
    def __init__(fname):
        self.file_name = file_name
        pass

    def parse_to_obj(self, file_name):
        file = open(file_name, 'r', encoding="utf8")
        return untangle.parse(file.read())

    def filter(self):
        pass


if __name__ == '__main__':
    files = sys.argv
    if len(files < 0):
        print "No file specified. Specify at least one file"
        exit(0)


    for item in files:
        print(" --- Analyzing " + item + " ---")
        file_name = item
        obj = XMLParser().parse_to_obj(file_name)

        for p in obj.mediawiki.page:
            print(p.title.cdata)
