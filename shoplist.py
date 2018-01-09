#coding=utf-8
import requests
import json
import urllib
import gevent
from gevent import monkey
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import setcookie
import jsondb


class Shoplist:

    @staticmethod
    def getShoplistPage(par1, par2, index, keyword, cookies):
        page = ''
        while not page:
            try:
                page = requests.get(url='https://shopsearch.taobao.com/search?isb=0&data-key=s&sort=sale-desc&app=shopsearch&ajax=true&q=' + keyword + '&data-value=' + str(index * 20) + par1 + par2,
                                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'},
                                    cookies=cookies).text
            except:
                continue
        try:
            page = json.loads(page)['mods']['shoplist']['data']['shopItems']
            return page
        except:
            return ''

    @staticmethod
    def getShoplist(con, table, keyword, cookie_str):
        keyword = urllib.quote(keyword)
        cookies = setcookie.Setcookie(cookie_str)
        jsondb_handler = jsondb.Jsondb(con, table)
        for par1 in ['jin', 'huang', 'zhuan', 'xin']: # &ratesum=
            for par2 in ['北京', '上海']: # &loc=
                index = 0
                is_end = False
                event_list = []
                while not is_end:
                    event_list.append(gevent.spawn(Shoplist.getShoplistPage, '&ratesum=' + par1, '&loc=' + urllib.quote(par2), index, keyword, cookies))
                    if len(event_list) == 100:
                        print par1, par2, 'Shoplist page', index + 1, 'fetched'
                        result = gevent.joinall(event_list)
                        for page in result:
                            if page.value:
                                jsondb_handler.toDB(page.value)
                            else:
                                is_end = True
                        event_list = []
                    index += 1

