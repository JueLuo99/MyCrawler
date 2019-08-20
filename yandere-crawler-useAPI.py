import os
import re
import requests
import time

# 下载路径，默认为该文件所在路径
downloadPath = os.path.abspath(os.path.dirname(__file__))
downloadPath += os.path.sep + time.strftime("%Y%m%d", time.localtime())

# 需要爬取的图片的 tag ， 默认为空
tag = ""
print("请输入想要爬取的 tag （不输入将会爬取全站）：")
tag = input()
if tag:
    tag = "tags=" + tag + "&"
print("\n准备就绪！")
os.system("pause")



def downloadPic(url):
    """
    保存目标图片
    """
    fileName = os.path.split(url)[1]
    fileName = fileName.replace("yande.re","")
    fileName = fileName.replace("%20","+")
    fileName = fileName.replace("+","",1)
    fileName = fileName.replace("+","_",1)
    with open(downloadPath+os.path.sep+fileName, 'wb') as file:
        file.write(requests.get(url).content)



# 创建工作空间
if not(os.path.exists(downloadPath)):
    os.mkdir(downloadPath)
print("创建目录 "+downloadPath)

# 默认从第 1 页开始爬取
page = 1

while True:
    # 构造目标网址，准备开始爬取
    url = "https://yande.re/post.json?" + tag + "page=" + str(page)

    response = requests.get(url)
   
    json = response.json()

    print("获取列表 " + "该页面共有 " + str(len(json)) + " 张图片")

    # 开始爬取并下载图片
    for i in json:
        print("开始下载 " + i["file_url"])
        downloadPic(i["file_url"])
    
    # 当前页面爬取完毕，开始准备爬取下一页
    page += 1
    print("\n切换页面 当前页面爬取完毕，开始爬取第" + str(page) + "页\n")


