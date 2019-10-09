# coding:utf-8
#@Time : 2019/10/02  22:56
#author : Around

import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

class DFS():
    # 属性
    def __init__(self):
        #1. 需要一个存放未采集url的容器---栈
        self.uncrawl_url = []
        #2. 需要一个存放已采集url的容器---列表、集合
        self.crawled = []

    #方法

    #1. 可以存未采集的url
    def save_uncrawl(self,url):
        if url not in self.crawled:
            self.uncrawl_url.append(url)

    #2. 可以取未采集url
    def get_uncrawl(self):
        return self.uncrawl_url.pop()

    #3. 可以存已采集的url
    def save_crawled(self,url):
        return self.crawled.append(url)

    #4. 判断当前栈是否为空
    def isempty(self):
        if not self.uncrawl_url:# 如果未采集的url不为空
            return True
        else:# 如果采集的url为空
            return False

### 爬虫
class Crawler():

#属性
    def __init__(self):
    #1. 存url的调度器
        self.dfs = DFS()

#方法
    #采集网页
    def crawl(self):
        self.dfs.save_uncrawl('http://www.baidu.com')
        while not self.dfs.isempty():
            url = self.dfs.get_uncrawl()
            self.dfs.save_crawled( url )
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
                        self.dfs.save_uncrawl(i)
                # url = self.dfs.get_uncrawl()
                print(self.dfs.crawled)
            except:
                pass

if __name__ == '__main__':
    Crawler().crawl()
