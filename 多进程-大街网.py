# coding:utf-8
#@Time : 2019/10/05  14:16
#author : Around
from lxml import etree
import pymongo
import requests
from multiprocessing import Pool,Manager
import time

conn = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = conn['dajie']
myset = mydb['dajiedata']

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'referer': 'https://so.dajie.com/job/search?keyword=%E9%94%80%E5%94%AE&from=job&clicktype=blank',
}
cookie = {
    'cookie': 'DJ_UVID=MTU2ODc4Njg4ODU4MTgzNTE4; _ga=GA1.2.630203741.1569240284; Hm_lvt_6822a51ffa95d58bbe562e877f743b4f=1569295545,1569321303,1569477754,1569496436; DJ_RF=https%3A%2F%2Fwww.dajie.com%2Fcorp%2F1000230%2Findex%2Fintro; DJ_EU=http%3A%2F%2Fwww.dajie.com%2Fcaptcha%2Fcode; dj_cap=96fe650462f9772ef5ece0e1a8f65cdf; _close_autoreg=1570266074487; _close_autoreg_num=4; SO_COOKIE_V2=fd98pl2vwixuwNuNjMvasdjylmXVtblxl78KKL+DzoaSYm+MmoBPGseJ/TTrmVvDRUPtnx+Mck4oAo8+CA8vb8NbcpB+EQ3Zv8rr'
}
def get_cookie():
    global cookie
    cookie = requests.get(url='https://so.dajie.com/job/search?keyword=%E9%94%80%E5%94%AE&from=job&clicktype=blank').cookies
    return cookie

def get_list(url_q):
    global cookie
    # url_q.put('around')
    pagenum = 1
    while 1:
        # print('list')
        url = 'https://so.dajie.com/job/ajax/search/filter?keyword=%E9%94%80%E5%94%AE&order=0&city=&recruitType=&salary=&experience=&page='+str(pagenum)+'&positionFunction=&_CSRFToken=&ajax=1'
        res = requests.get( url=url, headers=headers,cookies=cookie ).json()
        if not res:
            cookie = get_cookie()
            continue
        for i in res['data']['list']:
            url_q.put( i['jobHref'] )


def get_detail(url_q,data_q):
    # data_q.put(url_q.get())
    global cookie
    while 1:
        # print('detail')
        url = url_q.get()
        url = 'http:' + url
        # print(url)
        res = requests.get( url=url, headers=headers,cookies=cookie ).text
        ele = etree.HTML( res )
        jobname = ele.xpath( "//span[@class='job-name']/@title" )
        data_q.put( jobname[0] )

def save_db(data_q):
    # print(data_q.get())
    while 1:
        # print('db')
        jobname = data_q.get()
        data = {"jobname":jobname}
        print(1)
        myset.insert(data)

if __name__ == '__main__':
    pool = Pool(processes=3)#创建一个进程池，并且规定进程数
    url_q = Manager().Queue()
    data_q = Manager().Queue()
    pool.apply_async(func=get_list,args=(url_q,))#异步执行进程
    pool.apply_async(func=get_detail,args=(url_q,data_q))
    pool.apply_async(func=save_db,args=(data_q,))
    pool.close()
    pool.join()
