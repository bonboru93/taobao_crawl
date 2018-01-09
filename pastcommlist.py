#coding=utf-8
import requests
from lxml import html
import gevent
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Pastcommlist:
    def __init__(self, con, userid):
        self.con = con
        self.db = self.con.cursor()
        self.userid = userid
        self.db.execute('CREATE TABLE ' + self.userid + ' (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, word TEXT, title TEXT, link TEXT, price REAL, buyer TEXT, rate TEXT, cla INTEGER)')
        self.final_page = 800

    def getPastcommlistPage(self, index):
        delay = 0
        page = ''
        while not page:
            if index > self.final_page:
                return
            try:
                page = requests.get('https://ratehis.taobao.com/history?&userId=' + self.userid + '&page=' + str(index)).text
            except:
                print self.userid, 'page', index, 'sleep caused by request error'
                gevent.sleep(delay)
                delay += 3
                continue
            if page.find(u'买家：') < 0:
                if index == 1:
                    self.final_page = 0
                    print '=====', self.userid, 'Pastcommlist final page: 0'
                    return
                page = ''
                print self.userid, 'page', index, 'sleep caused by blank page error'
                gevent.sleep(delay)
                delay += 3
        if page[page.find('data-hasNext="') + len('data-hasNext="')] == '0':
            self.final_page = index
            print '=====', self.userid, 'Pastcommlist final page:', index
        comm_list = html.fromstring(page).xpath('//tr')
        skip_zero = True
        for comm in comm_list:
            if skip_zero:
                skip_zero = False
                continue
            date = comm.xpath('.//p[@class="comment"]/../p[@class="text-gray"]/text()')[0][1:-1]
            word = comm.xpath('.//p[@class="comment"]')[0].xpath('string()').strip()
            title = comm.xpath('.//a[contains(@href, "item.taobao.com")]/text()')[0]
            link = comm.xpath('.//a[contains(@href, "item.taobao.com")]/@href')[0]
            price = comm.xpath('.//span[@class="text-red"]/text()')[0]
            buyer = comm.xpath('.//a[contains(@href, "i.taobao.com")]/text()')[0].strip()
            try:
                rate = comm.xpath('.//img[contains(@src, "newrank/b_")]/@src')[0]
                rate = rate[rate.find('newrank/b_') + len('newrank/b_'): rate.find('.gif')]
            except:
                rate = '0'
            cla = comm.xpath('.//i[contains(@class, "icon-gnb-")]/@class')[0]
            cla = cla[cla.find('icon-gnb-') + len('icon-gnb-'):]
            self.db.execute("INSERT INTO " + self.userid + " VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (date, word, title, link, price, buyer, rate, cla))
        print self.userid, 'page', index, 'finished'

    def getPastcommlist(self):
        print '===== Fetching', self.userid, 'Pastcomment'
        index = 1
        event_list = []
        while index <= self.final_page:
            event_list.append(gevent.spawn(self.getPastcommlistPage, index))
            if len(event_list) == 10:
                gevent.joinall(event_list, timeout=300)
                self.con.commit()
                event_list = []
            index += 1
        if event_list:
            gevent.joinall(event_list, timeout=300)
            self.con.commit()
