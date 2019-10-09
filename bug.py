# coding:utf-8
#@Time : 2019/09/17  22:33
#author : Around
import time
from lxml import etree

import requests
import MySQLdb
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Referer': 'https://www.cnvd.org.cn/flaw/typelist?typeId=27',
    'Host': 'www.cnvd.org.cn',
    'Cookie': '__jsluid_s=750bf0c6717e8f5d1f536b8d2c0c1608; __jsluid_h=4618c0a8f21f787094b50212180c7667; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1568734641,1568770951; __jsl_clearance=1568854740.57|0|nv%2F30tbed4zuLUv6JEPmb7JgWnI%3D; JSESSIONID=2B47DA53B91BEE7C76ACC0171A2BD402'
}
data = {
    # 'typeId': '27'
}
proxies = {'http': '111.11.98.58:9000'}
count = 60
while 1:
    url = 'https://www.cnvd.org.cn/flaw/typeResult?typeId=27&max=20&offset='+str(count)
    re=requests.post(url=url,data=data,headers=headers,proxies=proxies).text
    # print(re)
    count+=20
    ele = etree.HTML(re)
    urls = ele.xpath('//td/a/@href')
    conn = MySQLdb.connect(host='127.0.0.1',port=3306,user='root',password='root',db='film',charset='utf8')
    cursor = conn.cursor()
    for url1 in urls:
        url1 = 'https://www.cnvd.org.cn'+url1
        time.sleep(5)
        re1 = requests.get(url=url1,headers=headers).text
        ele1 = etree.HTML(re1)
        aa = ele1.xpath( "//tr/td[2]/text()" )
        s = []
        for j in aa:
            if j.strip() != '':
                s.append( j.strip() )
        try:
            # print(s)
            cnvd_id = s[0]
            publish_date = s[1]
            danger_level = s[2].strip()[0:1]
            product = s[4]
            description = s[6]+s[5]
            type = s[7]
            link = s[9]
            # print(cnvd_id,publish_date,danger_level,product,description,type,link)
            # print(description)
            sql = "insert into bug values(%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,[cnvd_id,publish_date,danger_level,product,description,type,link])
            conn.commit()
        except:
            pass
"""
['CNVD-2019-31055', '2019-09-11', 
 '低\r\n\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t(', ')', 
 'Microsoft Windows 10 1703', 'Microsoft Windows 10 1709', 'Microsoft Windows Server 1709', 
 'Microsoft Windows 10 1803', 'Microsoft Windows Server 1803', 'Microsoft Windows Server 2019', 
 'Microsoft Windows 10 1809', 'Microsoft Windows和Microsoft Windows Server都是美国微软（Microsoft）公司的产品。Microsoft Windows是一套个人设备使用的操作系统。Microsoft Windows Server是一套服务器操作系统。Windows Kernel是其中的一个Windows系统内核。', 
 'Microsoft Windows kernel中存在信息泄露漏洞，未授权的攻击者可利用漏洞获取受影响组件敏感信息。', '通用型漏洞', '厂商已发布了漏洞修复程序，请及时关注更新：',
 'https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2019-0840', '(暂无验证信息)', 
 '2019-04-10', '2019-09-11', '2019-09-11', '(无附件)', '低', '部分地', '不受影响']
"""