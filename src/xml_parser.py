import untangle


class XMLParser:
    def __init__(self):
        pass

    def parse_to_obj(self, file_name):
        file = open(file_name, 'r', encoding="utf8")
        return untangle.parse(file.read())

    def filter(self):
        pass


if __name__ == '__main__':
    file_name = '../data/nogamenolife_pages_current.xml'
    test_file = '../data/test.xml'

    obj = XMLParser().parse_to_obj(file_name)

    for p in obj.mediawiki.page:
        print(p.title.cdata)
