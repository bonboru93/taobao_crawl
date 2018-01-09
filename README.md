# taobao_crawl
淘宝爬虫汇总

## process.py
【关键词 -> 店铺列表 -> 店铺资质 -> 半年历史评论】系列的总入口

## shoplist.py
不论请求店铺列表的参数为何，最多返回250页，也即5000家店。通过增加店铺资质和所在省市的参数限制可以获取到更多的店铺地址。</br>
使用gevent协程库并发100个请求，最佳协程数量多少需再探讨。</br>
注意全程统一编码。

## jsondb.py
解析店铺信息的json档，写入sqlite。</br>
回溯解json嵌套，用下划线隔开。</br>
根据json内容增加db列，处理某些店铺缺失的值。</br>
未将db实例加锁，不可并行。

## shopquality.py
找到一个cdn地址链接不做机器人检查，店铺资质内容写在js输出的html中。</br>
处理js输出自带的转义符号后，直接xpath解析，得到资质描述串。</br>
同样适用gevent。

## pastcommlist.py
采用 threading + gevent 模式，10线程 * 10 协程。</br>
半年前的评论入口不检查机器人。</br>
服务器以响应时间来限制爬虫，可能返回虚假的“已达最后一页”的结果，使用【页面至少有一条评论，且翻页按钮不可用】作为到达最后一页的判定。</br>
到达最后一页后写入final_page变量，通知在爬更高页码的协程停止。</br>
超过1000页以后响应非常慢，最多大致能抓到1500页内容，为保证效率，批处理作业时限定800页上限。</br>
在requests超时或返回虚假页面后设定delay，delay逐次增加，同时设定协程的总超时时间。</br>
页面内容使用xpath获取，xpath规则不要使用浏览器自动生成的，观察多个页面，写出适应性最好的规则，最后还是要处理意外的缺失。

## checkcodebypass.py

