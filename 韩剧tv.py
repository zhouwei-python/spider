# coding:utf-8
#@Time : 2019/10/01  18:35
#author : Around
import re

import os
import requests
from requests_html import HTML,HTMLSession
from Crypto.Cipher import AES
# 进入列表界面
def play_tv(response):
    # 判断是否有此剧
    tips = response.html.xpath("//div[@class='no_data']/p/text()")
    try:
        if tips[0].startswith('暂无'):
            print("没有此剧")
    except:
        # 找到关于输入剧名的所有剧
        tv_title = response.html.find('h3 a')
        for title in tv_title:
            # 只有当剧名和输入的相等，才继续
            if tv_name == title.attrs['title']:
                # 有的话，找到立即播放的url
                tv_url = title.attrs['href']
                # 因为url不完整，需要拼接成完整的url
                tv_full_url = "http://www.hanjutv.com"+tv_url
                # 发送请求并得到响应
                response1 = session.get(tv_full_url)
                # 此时进入选集页面，将响应交给xuanji()函数处理
                xuanji(response1.text)
        else:
            print("请输入正确的剧名，一个字也不能差哦！")
# 进入选集页面
def xuanji(response1):
    # 通过正则匹配到每一集的url，返回一个列表
    res = re.findall(r'target="_blank" href="(.*)">', response1)
    # res = response1.html.find("div ul li a")
    for i in res:
        # 获取referer所需要的值
        num = re.findall("\d+",i)
        headers = {
            'Host': 'ww4.hanjutv.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3921.0 Safari/537.36',
            'Referer': 'https://www.hanjutv.com/player/'+str(num[0])+'.html'
        }
        # 因为每个url不完整，要拼接成完整的url
        full_url = 'http://www.hanjutv.com'+i
        # 对拼完的每一集的url发请求，
        response2 = session.get(full_url)
        # 进入播放页面
        download(response2,headers)
# 进入播放页面
def download(response2,headers):
    # url_h = response2.html.find('iframe')[0].attrs['src']
    # 找到'播发器'里面的url，因为这个url对应的页面有一个url，这个url是获取视频片段的所有js
    url_h = re.findall(r'height="100%" src="(.*)" frameborder="0"', response2.text)
    # 同样拼凑成完整的url
    full_url_h = 'https:'+url_h[0]
    # 发送请求，这里一定要加headers，否则获取不到页面完整信息
    res1 = requests.get(url=full_url_h,headers=headers)
    # 接收响应后，获取script中url键对应的值(是一个url)，这个url就是如上所说要获取视频片段的所有js
    url_video = re.findall( r"url:'(.*)',", res1.text )
    # print( url_video )
    if url_video:
        # 获取key所需参数
        size = url_video[0].split('/')[5]
        # 根据此url获取片段
        slice_video = session.get(url_video[0])
        # 如下是为了拼凑key，进行解密操作
        play_path = response2.html.find('iframe')[0].attrs['src'][41:].split('/')
        key_url  = 'http://'+play_path[0]+'/'+play_path[1]+'/'+play_path[2]+'/'+str(size)+'/hls/key.key'
        res_key = session.get(key_url).content
        cryptor = AES.new( res_key, AES.MODE_CBC, res_key )
        # 获取每一个片段js
        deal_slice_videos(slice_video.text,cryptor)
    else:
        print("视频播放错误，下载失败")
        return
# 解决分散的片段js
def deal_slice_videos(slice_video,cryptor):
    # 将片段的js全部取出，放入列表中
    urls = []
    for i in slice_video.split( '\n' ):
        if re.findall( "^[https].+[js]$", i ):
            urls.append( i )
    urls = ['http' + i[5:] for i in urls]
    get_in_file(urls,cryptor)
# 保存到文件中
def get_in_file(urls,cryptor):
    count = 1
    print("正在下载" + tv_name + "第%d集"%count)
    for t_url in range( len( urls ) ):
        data = session.get( url=urls[t_url] )
        # print(cryptor.decrypt( data.content ))
        with open( '韩剧tv/'+tv_name+'第'+str(count)+'集.mp4', 'ab+' ) as w:
            w.write( cryptor.decrypt( data.content ) )
        print( t_url + 1, len( urls ) )
    count+=1
if __name__ == '__main__':
    if not os.path.exists('韩剧tv'):
        os.makedirs('韩剧tv')
    session = HTMLSession()
    tv_name = input("请输入剧名：")
    # tv_name = '天空之城'
    url = 'http://www.hanjutv.com/index.php?c=so&module=&keyword='+tv_name
    response = session.get(url)
    # 接收响应后，跳到列表界面
    play_tv(response)
