import datetime as dt
import xmltodict

class XMLParser:
    def __init__(self, fname, snapshot_time=dt.datetime.now()):
        self.file_name = fname
        self.time = snapshot_time
        self.data_obj = None

    def parse_to_obj(self, xml_attribs=True):
        print("Parsing File: " + self.file_name)
        with open(self.file_name, "rb") as f:  # notice the "rb" mode
            d = xmltodict.parse(f, xml_attribs=xml_attribs)
            self.data_obj = d
            return d

    def should_keep(self, node_title):
        IGNORE_LIST_PREFIX = ['Talk:', 'User:', 'File:', 'Thread:', 'Category:', 'Board Thread:', 'Template:',
                              'Category talk:', 'MediaWiki:', 'User blog comment:', 'Message Wall:', 'User blog:',
                              'Forum:', 'Board:', 'Help:', 'User talk:', 'Blog:', 'Top 10 list:', 'Template talk:',
                              'Portal:', 'File talk:', 'League of Legends Wiki:', 'Guide talk:', 'MediaWiki talk:',
                              'Top 10 list talk:', 'General Discussion/', 'HOC:', 'Questions and Answers/',
                              'News and Announcements/', 'Inception Wiki:', 'Gallery:', 'Apple Wiki:', 'Welcome:',
                              'Help talk:', 'Parks and Recreation Wiki:', 'Module:', 'League of Legends Wiki talk:',
                              'Taylor Swift Wiki/', 'Fanon talk:', 'Film talk:', 'Fanon:', 'Baker Street Wiki:', 
                              'Baker Street Wiki talk:', 'Faulty Towers Wiki:', 'Blog talk:', 'Bones Wiki:', 'Bones Wiki talk:',
                              'Breaking Bad Wiki:', 'Breaking Bad Wiki talk:', 'Code Geass Wiki:', 'New on Code Geass Wiki/', 
                              'Message Wall Greeting:', 'Wiksteria Lane:', 'Wiksteria Lane talk:', 'Fr:', 'Gilmore Girls Wiki:',
                              'Haruhi Wiki:', 'Haruhi Wiki talk:', 'How I Met Your Mother Wiki:', 'Quiz:', 'QuizArticle:',
                              'How I Met Your Mother Wiki talk:', 'HW:', 'Form:', 'Modern Family Wiki:', 
                              'Modern Family Wiki talk:', 'Everybody Loves Raymond:', 'Sons of Anarchy:', 'Bradypedia:', 'Forum talk:', 
                              'Twin Peaks Wiki:', 'Twin Peaks Wiki talk:', 'TYPE-MOON Wiki:', 'TYPE-MOON Wiki talk:' ]
        IGNORE_LIST_SUFFIX = [':Templates', ':Copyrights', ':Candidates for speedy deletion', ':Privacy policy',
                              ':Administrators', ':Navigation', ':Bureaucrats', ':Community Portal',
                              ':Terminology List', ':Sandbox', ':Welcome', ':Policy', ':Protected page',
                              '/Unofficial Chat', ':About', '/List']

        for item in IGNORE_LIST_PREFIX:
            if node_title[0:len(item)] == item:
                return False

        for item in IGNORE_LIST_SUFFIX:
            if node_title[len(node_title) - len(item): len(node_title)] == item:
                return False

        return True

    def update_time(self, new_time):
        self.time = new_time

    def find_oldest_time(self):
        oldest_time = None
        if not self.data_obj:
            obj = self.parse_to_obj()
        else:
            obj = self.data_obj
        for p in obj["mediawiki"]["page"]:
            if not 'revision' in p:
                return oldest_time
            rev = p['revision']
            if not 'text' in rev:
                for item in rev:
                    time = item['timestamp']
                    # format is 2014-12-17T02:25:15Z
                    time_obj = dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
                    if not oldest_time or time_obj < oldest_time:
                        oldest_time = time_obj
        return oldest_time

    def parse_to_dict(self):
        is_snapshot = False
        data_return = {}
        if not self.data_obj:
            obj = self.parse_to_obj()
        else:
            obj = self.data_obj
        for p in obj["mediawiki"]["page"]:
            if not 'revision' in p:
                continue
            rev = p['revision']
            if not 'text' in rev:
                is_snapshot = True
                latest_text = None
                latest_time = None
                for item in rev:
                    time = item['timestamp']
                    # format is 2014-12-17T02:25:15Z
                    time_obj = dt.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
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
            if not text_obj:
                continue
            if not '#text' in text_obj:
                continue
            name = p['title'].strip()
            if not self.should_keep(name):
                continue
            text = text_obj['#text']

            data_return[name] = text

        if is_snapshot:
            print("Snapshot Date: " + str(self.time))
        else:
            print("Latest Snapshot")
        return data_return
