from PIL import Image
from io import BytesIO
import setcookie
import requests
import urllib
from lxml import html
from pytesseract import *
pytesseract.tesseract_cmd = r'.\Tesseract-OCR\tesseract'


def checkcodepass(page, cookie_str):
    if page.find('anti_Spider') < 0:
        return page
    cookies = setcookie.setcookie(cookie_str)

    pos = page.find('sessionid=')
    sessionid = page[pos + len('sessionid='): page.find('&', pos)]

    page = html.fromstring(page)
    smReturn = urllib.quote(page.xpath('//input[@name="smReturn"]/@value')[0])
    smTag = urllib.quote(page.xpath('//input[@name="smTag"]/@value')[0])
    smSign = urllib.quote(page.xpath('//input[@name="smSign"]/@value')[0])

    img_url_base = 'https://pin.aliyun.com/get_img?identity=sm-ratemanager&type=number&sessionid='
    check_url_base = 'https://sec.taobao.com/query.htm?action=QueryAction&event_submit_do_query=ok&smPolicy=ratemanager-srp-anti_Spider-html-checkcode&smApp=ratemanager&smReturn=' + smReturn + '&smCharset=GBK&smTag=' + smTag + '&captcha=&smSign=' + smSign + '&identity=sm-ratemanager' + '&checkcode='

    while True:
        print 'Auto checkcode bypass'
        checkcode = requests.get(img_url_base + sessionid).content
        im = Image.open(BytesIO(checkcode))
        im = im.convert('L')
        checkcode = pytesseract.image_to_string(im, config='digits -psm 7').replace(' ', '')
        page = requests.get(url=check_url_base + str(checkcode),
                            cookies=cookies).text

        if page.find('anti_Spider') < 0:
            return page

if __name__ == '__main__':
    page = requests.get(url='https://rate.taobao.com/user-rate-UvCkuMCcyvFH0OQTT.htm',
                        cookies=setcookie.setcookie('cna=947CElSjIwECAYxwHYHyKs8t; _m_h5_tk=1c812277104797b12811ab249a057897_1513859432034; _m_h5_tk_enc=0623283c458f052fe63eacbcf3e90af4; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _tb_token_=7R6oA6whcG3q6jhvrOFV; v=0; uc1=cookie14=UoTdf1ES6hnMew%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=UtASsssme%2BBq&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; uc3=sg2=UoNq121n88ElErR6FaJA9S%2BJW7lNvFr%2BDn8V5kORlE0%3D&nk2=EFVSErMvg62JM9LE&id2=UU6jWKzZfErj&vt3=F8dBzLbVzPYu0aX2sK4%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTUxNDAzMTg5Nw%3D%3D; uss=U7emCe7r6dskP7%2FfwyztZuLRi%2FGEDZ%2FUuRpcb4tj5lJqh9Xj11tZB3MXKuQ%3D; lgc=skyline80386; tracknick=skyline80386; cookie2=3e461fbaf8494f301f0a1b9198a6ada3; sg=671; mt=np=&ci=1_1; cookie1=WvNHTbWjAGwnTE%2FwnukjndjnAhBAGvU3xJ5mzKY74PQ%3D; unb=262047697; skt=40cea8cc6067b8de; t=ad8acb3ed3d904c9fd48afd764fcdd5c; publishItemObj=Ng%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=skyline80386; cookie17=UU6jWKzZfErj; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261514034344928; isg=Anx8i4a_CjEGoD7ophXsSPcETRoudSCfk8yONFb9qGdKIR2rfoUTLyWZZX6j')).text
    checkcodepass(page, 'cna=947CElSjIwECAYxwHYHyKs8t; _m_h5_tk=1c812277104797b12811ab249a057897_1513859432034; _m_h5_tk_enc=0623283c458f052fe63eacbcf3e90af4; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _tb_token_=7R6oA6whcG3q6jhvrOFV; v=0; uc1=cookie14=UoTdf1ES6hnMew%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=UtASsssme%2BBq&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; uc3=sg2=UoNq121n88ElErR6FaJA9S%2BJW7lNvFr%2BDn8V5kORlE0%3D&nk2=EFVSErMvg62JM9LE&id2=UU6jWKzZfErj&vt3=F8dBzLbVzPYu0aX2sK4%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D; existShop=MTUxNDAzMTg5Nw%3D%3D; uss=U7emCe7r6dskP7%2FfwyztZuLRi%2FGEDZ%2FUuRpcb4tj5lJqh9Xj11tZB3MXKuQ%3D; lgc=skyline80386; tracknick=skyline80386; cookie2=3e461fbaf8494f301f0a1b9198a6ada3; sg=671; mt=np=&ci=1_1; cookie1=WvNHTbWjAGwnTE%2FwnukjndjnAhBAGvU3xJ5mzKY74PQ%3D; unb=262047697; skt=40cea8cc6067b8de; t=ad8acb3ed3d904c9fd48afd764fcdd5c; publishItemObj=Ng%3D%3D; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; _l_g_=Ug%3D%3D; _nk_=skyline80386; cookie17=UU6jWKzZfErj; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; whl=-1%260%260%261514034344928; isg=Anx8i4a_CjEGoD7ophXsSPcETRoudSCfk8yONFb9qGdKIR2rfoUTLyWZZX6j')
