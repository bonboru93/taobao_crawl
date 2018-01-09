#coding=utf-8
import sqlite3
import json
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import shoplist
import pastcommlist
import shopquality

db_name = 'auto8'
shop_table = 'shop'
shop_quality_table = 'quality'
keyword = '自动发货'
cookie_str = 'cna=947CElSjIwECAYxwHYHyKs8t; v=0; _m_h5_tk=1c812277104797b12811ab249a057897_1513859432034; _m_h5_tk_enc=0623283c458f052fe63eacbcf3e90af4; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; uc3=sg2=UoNq121n88ElErR6FaJA9S%2BJW7lNvFr%2BDn8V5kORlE0%3D&nk2=EFVSErMvg62JM9LE&id2=UU6jWKzZfErj&vt3=F8dBzLbX5vptfUcHkIs%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTUxMzg1ODQ2NA%3D%3D; lgc=skyline80386; tracknick=skyline80386; cookie2=113be2826d8c4d9c1d367cff19ef416d; skt=ec7c88be3f5bf6ff; t=ad8acb3ed3d904c9fd48afd764fcdd5c; publishItemObj=Ng%3D%3D; _cc_=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=1_1; _tb_token_=ed5ee4b5ae131; whl=-1%260%260%261513859012177; uc1=cookie14=UoTdeAQ2cKEYzA%3D%3D&lng=zh_CN&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&existShop=false&cookie21=W5iHLLyFe3xm&tag=8&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0; swfstore=127447; isg=Aj4-RbG76NVmcjz2uE8ObqHuj1SAfwL5pZYMiuhHqgF8i95lUA9SCWRpZ2C9; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=9B94930140A6DAC6377E61010FCD3D45'
con = sqlite3.connect(db_name + '.db')

shoplist.Shoplist.getShoplist(con, shop_table, keyword, cookie_str)

numberId_list = []
total_comm = 0
for current_shop in con.execute('SELECT uid,dsrInfo_dsrStr from ' + shop_table):
    numberId_list.append(current_shop[0])
    current_comm = int(json.loads(current_shop[1])['srn']) / 40
    total_comm += min(current_comm, 800)

#shopquality.getShopQuality(con, shop_quality_table, numberId_list)


class CallPastcommlist(threading.Thread):
    def __init__(self, con, userid):
        threading.Thread.__init__(self)
        self.pastcommlist_ptr = pastcommlist.Pastcommlist(con, userid)

    def run(self):
        self.pastcommlist_ptr.getPastcommlist()

threads = []
finished_comm = 0
for current_shop in con.execute('SELECT userRateUrl,dsrInfo_dsrStr from ' + shop_table):
    pos = current_shop[0].find('user-rate-')
    userId = current_shop[0][pos + len('user-rate-'): current_shop[0].find('.htm')]
    current_comm = int(json.loads(current_shop[1])['srn']) / 40
    finished_comm += min(current_comm, 800)
    thread = CallPastcommlist(con, userId)
    thread.start()
    threads.append(thread)
    if len(threads) == 10:
        for thread in threads:
            thread.join()
        threads = []
        print 'Finished percent: ', 100 * float(finished_comm) / total_comm
for thread in threads:
    thread.join()
