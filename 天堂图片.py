# coding:utf-8
#@Time : 2019/10/02  17:26
#author : Around
import re

import os
from requests_html import HTMLSession
session = HTMLSession()
count = 1
# 处理第一次响应的结果
def deal_res(response):
    # 解析图片的url
    img_url = response.html.xpath("//div[@class='il_img']/a/@href")
    for url in img_url:
        # url不完整，需要进行拼接
        full_img_url = 'http://ivsky.com'+url
        # 对拼接好的图片url发请求，接响应
        images = session.get(full_img_url)
        # 给到get_big_image()函数获取大图
        get_big_image(images)
# 处理第二次响应的结果，用于获取大图
def get_big_image(images):
    # 解析出大图的url
    big_images = images.html.xpath("//img[@id='imgis']/@src")
    for img in big_images:
        # url不完整，进行拼接
        img_path = 'http:'+img
        # 对拼接好的大图url发请求，接响应
        response_img = session.get(img_path).content
        # 调用write_into_file()进行写文件操作
        write_into_file(response_img)
# 写入文件
def write_into_file(response_img):
    global count
    # 打开一个流
    with open('天堂图片/'+str(count)+'.jpg','wb') as w:
        # 将大图以二进制的形式写入文件
        w.write(response_img)
    print("已经下载好%d张"%count)
    count += 1

if __name__ == '__main__':
    # 创建文件夹，名为"天堂图片"
    if not os.path.exists('天堂图片'):
        os.makedirs('天堂图片')
    # 进行分页
    page = 1
    while 1:
        if page == 1:
            url = 'https://www.ivsky.com/bizhi/mei_nv_t10/'
        else:
            url = 'https://www.ivsky.com/bizhi/mei_nv_t10/index_'+str(page)+'.html'
        page += 1
        # 发请求，接响应
        response = session.get(url)
        # 给到deal_res进行响应处理
        deal_res(response)
