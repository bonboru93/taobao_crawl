#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Jsondb:
    def __init__(self, con, table):
        self.con = con
        self.db = con.cursor()
        self.table = table
        self.keys = []

        self.con.text_factory = str
        self.db.execute('CREATE TABLE ' + self.table + ' (aiid INTEGER PRIMARY KEY AUTOINCREMENT)')

    def parseItem(self, pre, json_obj):
        result = {}
        for key in json_obj:
            if type(json_obj[key]) == dict:
                result = dict(result, **self.parseItem(pre + key + '_', json_obj[key]))
            else:
                json_obj[key] = str(json_obj[key])
                result[pre + key] = json_obj[key]
        return result

    def toDB(self, json_obj):
        for item in json_obj:
            parsed_item = self.parseItem('', item)
            values = []
            for key in self.keys:
                try:
                    values.append(parsed_item.pop(key))
                except:
                    values.append(' ')
            for key in parsed_item:
                self.keys.append(key)
                self.db.execute('ALTER TABLE ' + self.table + ' ADD ' + key + ' TEXT DEFAULT " "')
                values.append(parsed_item[key])
            self.db.execute('INSERT INTO ' + self.table + ' VALUES(NULL' + ',?' * len(self.keys) + ')', values)
        self.con.commit()
