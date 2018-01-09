#coding=utf-8
import requests
from lxml import html
import gevent
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getShopQualityPage(con, table, numberId):
    db = con.cursor()
    db.execute('CREATE TABLE IF NOT EXISTS ' + table + ' (numberId TEXT PRIMARY KEY, quality TEXT)')
    page = ''
    while not page:
        try:
            page = requests.get('https://hdc1.alicdn.com/asyn.htm?userId=' + numberId).text
        except:
            continue
    pos = page.find(r'<div class=\"icon-box\">')
    if pos < 0:
        db.execute('INSERT INTO ' + table + ' VALUES(?, ?)', (numberId, ' '))
    else:
        page = page[pos: page.find('</div>', pos) + len('</div>')].replace(r'\"', '"').replace(r'\n', '').replace(r'\r', '')
        page = html.fromstring(page).xpath('//li')
        result = ''
        for item in page:
            result += item.xpath('string()').replace(' ', '') + ';'
        db.execute('INSERT INTO ' + table + ' VALUES(?, ?)', (numberId, result))
    con.commit()
    print numberId, 'Shop quality done'


def getShopQuality(con, table, numberId_list):
    print '===== Fetching Shop quality'
    event_tot = 0
    event_list = []
    for numberId in numberId_list:
        event_list.append(gevent.spawn(getShopQualityPage, con, table, numberId))
        event_tot += 1
        if event_tot == 1000:
            gevent.joinall(event_list)
            event_tot = 0
            event_list = []
    if event_tot > 0:
        gevent.joinall(event_list)