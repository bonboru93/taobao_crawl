#coding=utf-8
import requests
from lxml import html
import json
import sqlite3
import setcookie
import checkcodepass
import time

def shopdetail(db_name, userid, cookie_str):
    con = sqlite3.connect(db_name + '.db')
    db = con.cursor()
    try:
        db.execute('CREATE TABLE `shop_detail` (`userid` TEXT NOT NULL, `title` TEXT, `url` TEXT, `sold` INTEGER, `procnt` INTEGER, `mainauction` TEXT, PRIMARY KEY(`userid`))')
    except:
        pass
    cookies = setcookie.setcookie(cookie_str)
    page = requests.get(url='https://rate.taobao.com/user-rate-' + userid + '.htm',
                        cookies=cookies).text
    page = checkcodepass.checkcodepass(page, cookie_str)
    page = html.fromstring(page)
    shopid = page.xpath('//input[@id="J_ShopIdHidden"]/@value')[0]
    charge = page.xpath('//div[@class="charge"]/span/text()')[0].replace(u'￥', '').replace(',', '')
    sep = page.xpath('//ul[@class="sep"]/li[1]')[0].xpath('string()')
    sep = sep[sep.find(u'卖家信用：') + len(u'卖家信用：'):].strip()
    currentAuction = page.xpath('//a[contains(@href, "//service.taobao.com/support")]/text()')[0].strip()
    quality_list = page.xpath('//ul[@class="quality"]//img/@title')
    quality_str = ''
    for quality in quality_list:
        quality_str += quality + ';'
    page = requests.get(url='https://rate.taobao.com/ShopService4C.htm?userNumId=' + userid + '&shopId=' + shopid,
                        cookies=cookies).text
    page = json.loads(page)
    avgRefund = page['avgRefund']['localVal']
    complaints = page['complaints']['localVal']
    refundSumNum = page['complaints']['refundSumNum']
    taobaoSolveNum = page['complaints']['taobaoSolveNum']
    punish = page['punish']['localVal']
    weibeiTimes = page['punish']['weibeiTimes']
    xujiaTimes = page['punish']['xujiaTimes']
    ratRefund = page['ratRefund']['localVal']
    refundCount = page['ratRefund']['refundCount']
    print shopid, charge, sep, currentAuction, quality_str, avgRefund, complaints, refundSumNum, taobaoSolveNum, punish, weibeiTimes, xujiaTimes, ratRefund, refundCount


if __name__ == '__main__':
    for i in range(0, 100):
        shopdetail('app4', 'UvCkuMCcyvFH0OQTT', 'cna=947CElSjIwECAYxwHYHyKs8t; _m_h5_tk=1c812277104797b12811ab249a057897_1513859432034; _m_h5_tk_enc=0623283c458f052fe63eacbcf3e90af4; thw=cn; _tb_token_=7R6oA6whcG3q6jhvrOFV; swfstore=41707; hng=CN%7Czh-CN%7CCNY%7C156; v=0; uc3=sg2=UoNq121n88ElErR6FaJA9S%2BJW7lNvFr%2BDn8V5kORlE0%3D&nk2=EFVSErMvg62JM9LE&id2=UU6jWKzZfErj&vt3=F8dBzLbVzdz0TzYr0jk%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTUxNDA0MDE0Nw%3D%3D; uss=U7emCe7r6dskP7%2FfwyztZuLRi%2FGEDZ%2FUuRpcb4tj5lJqh9Xj11tZB3MXKuQ%3D; lgc=skyline80386; tracknick=skyline80386; cookie2=3e461fbaf8494f301f0a1b9198a6ada3; sg=671; cookie1=WvNHTbWjAGwnTE%2FwnukjndjnAhBAGvU3xJ5mzKY74PQ%3D; unb=262047697; skt=e36c19cd9db4b182; t=ad8acb3ed3d904c9fd48afd764fcdd5c; publishItemObj=Ng%3D%3D; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=skyline80386; cookie17=UU6jWKzZfErj; mt=ci=1_1; uc1=cookie14=UoTdf1EVr3nRrA%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=VT5L2FSpczFp&tag=8&cookie15=URm48syIIVrSKA%3D%3D&pas=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; isg=AggI52EmxhWVaSqU0lHQ7CuY2XYasWy7f8D6aMK5MQNknagHasE8S56fcUIX; whl=-1%260%260%261514040172972')
