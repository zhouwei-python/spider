# coding:utf-8
#@Time : 2019/10/02  23:44
#author : Around

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
# 容器类---对容器的相关操作
class BFS():
    # 属性
    def __init__(self):
        self.uncrawl_url = []
        #1. 需要一个存放未采集url的容器---栈
        self.crawled = []
        #2. 需要一个存放已采集url的容器---列表、集合

    #方法

    #1. 可以存未采集的url
    def save_uncrawl(self,url):
        if url not in self.crawled:
            self.uncrawl_url.append(url)

    #2. 可以取未采集url
    def get_uncrawl(self):
        return self.uncrawl_url.pop(0)

    #3. 可以存已采集的url
    def save_crawled(self,url):
        return self.crawled.append(url)

    #4. 判断当前栈是否为空
    def isempty(self):
        if not self.uncrawl_url:
            return True
        else:
            return False

### 爬虫类
class Crawler():

#属性
    def __init__(self):
    #1. 存url的调度器
        self.bfs = BFS()

#方法
    #采集网页
    def crawl(self):
        self.bfs.save_uncrawl('http://www.baidu.com')
        while not self.bfs.isempty():
            url = self.bfs.get_uncrawl()
            self.bfs.save_crawled( url )
            try:
                print(url)
                res = requests.get(url=url, headers=headers,timeout=3).content.decode()
                ele = etree.HTML(res)
                title = ele.xpath('//title/text()')[0]
                print(title)
                urls = ele.xpath('//a/@href')
                for i in urls:
                    i = str(i)
                    if (i.__contains__('http://') or i.__contains__('https://')) and not i.__contains__('static-files'):
                        self.bfs.save_uncrawl(i)
                # url = self.bfs.get_uncrawl()
            except:
                pass

if __name__ == '__main__':
    Crawler().crawl()
