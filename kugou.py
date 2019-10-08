# coding:utf-8
#@Time : 2019/09/27  18:43
#author : Around
import json

import re

import os
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'Referer': 'https://www.kugou.com/yy/html/search.html',
}
def get_info(res):
    res_json = json.loads(res)
    for i in res_json['data']['lists']:
        try:
            music_name = i["FileName"].replace("<em>",'').replace("</em>",'')
            album_id = i['AlbumID']
            file_hash = i['FileHash']
            url1 =  "http://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash={}".format(file_hash)
            res1 = requests.get(url=url1,headers=headers).json()
            download_url = res1['url']
            print("即将下载---%s"%music_name)
            download(download_url,music_name)
        except:
            print('哈哈，宝贝儿，你没资格下载哦！')

def download(download_url,music_name):
    res2 = requests.get( url=download_url, headers=headers ).content
    print( "正在下载---%s" % music_name )
    with open('酷狗music/'+music_name+'.mp3','wb') as w:
        w.write(res2)
    print("%s---已经下载完毕\n"%music_name)

if __name__ == '__main__':
    if not os.path.exists( '酷狗music' ):
        os.makedirs( '酷狗music' )
    music_name = input("请输入你要下载的歌曲名：")
    url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery112407288139861568368_1569582001731&keyword=' + str(music_name ) + '&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1569582001733'
    res = requests.get( url=url ).text
    res1 = res[42:-2]
    get_info(res1)
