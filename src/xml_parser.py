import untangle


file_name = '../data/nogamenolife_pages_current.xml'
test_file = '../data/test.xml'

file = open(file_name, 'r', encoding="utf8")
obj = untangle.parse(file.read())
for p in obj.mediawiki.page:
    print(p.title.cdata)