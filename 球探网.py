# coding:utf-8
#@Time : 2019/09/25  09:12
#author : Around
from lxml import etree

import requests
import MySQLdb

headers ={
    'Referer': 'http://live.win007.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}
def getID():
    url = 'http://data.win007.com/soccer_scheduleid.js'
    re = requests.get(url=url,headers=headers).text
    result = re.split(';')[0][23:-1]
    result1 = result.split(',')
    return result1
def get_url():
    url_prefix = 'http://vip.win007.com/AsianOdds_n.aspx?id='
    ids = getID()
    conn = MySQLdb.connect( host='127.0.0.1', port=3306, user='root', password='root', db='film', charset='utf8' )
    cursor = conn.cursor()
    for i in ids:
        print(i)
        re = requests.get(url=url_prefix+i,headers=headers).text
        ele = etree.HTML(re)
        name = ''.join(ele.xpath("//title/text()")[0].split()[0:4])
        date = ele.xpath("//div[@class='row']/text()")[1].strip()
        try:
            for j in range(2,1000): # tr
                for k in range(1,13): # td
                    # s = ele.xpath( "//*[@id='oddsDetail']/tr[2]/td["+str(k)+"]/text()" )
                    s = ele.xpath("//table[@id='oddsDetail']/tr[" + str(j) + "]/td["+ str(k) +"]/text()")
                    if s:
                        # 赔率
                        pei = ele.xpath("//table[@id='oddsDetail']/tr[" + str(j) + "]/td["+ str(k) +"]/span/text()")
                        pei = pei[0] +' '+ pei[1]
                    else:
                        pei = '0'+' '+'0'
                        s=['']
                        # 公司
                        company = ele.xpath( "//*[@id='oddsDetail']/tr[1]/td[" + str( k ) + "]/text()" )
                        # 变化时间
                        time = ele.xpath( "//*[@id='oddsDetail']/tr["+str(j)+"]/td[14]/text()" )
                        time = time[0]+' '+time[1]
                        # 比分
                        score = ele.xpath( "//*[@id='oddsDetail']/tr["+str(j)+"]/td[13]/text()" )
                        if not score:
                            score = '0-0'
                        else:
                            score = score[0]
                    # print(name,date,s[0],company[0],pei,time,score)
                    sql1 = "insert into qiutan values(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql1,[name,date,company[0],s[0]+pei,time,score])
                    conn.commit()
        except:
            print('出错了')
get_url()

