import os
import re
import requests
import time

# 下载路径，默认为该文件所在路径
downloadPath = os.path.abspath(os.path.dirname(__file__))
downloadPath += os.path.sep + time.strftime("%Y%m%d", time.localtime())

def downloadPic(url, fileName):
    # 保存图片
    print("正在下载 " + fileName)
    # fileName = downloadCount + 1
    with open(downloadPath+os.path.sep+fileName, 'wb') as file:
        file.write(requests.get(url).content)


def getPicUrl():
    print("正在获取 ...")
    response = requests.get("http://yunjie.f06.87yun.club/st/r/")
    pattern = re.compile(r'<img src="[a-zA-z]+://[^\s]*')
    downloadURL = pattern.search(response.text).group(0).replace('<img src="',"").replace('"',"")
    name = os.path.basename(downloadURL)
    downloadPic(downloadURL, name)


# 创建工作空间
if not(os.path.exists(downloadPath)):
    os.mkdir(downloadPath)
print("创建目录 "+downloadPath)


while True:
    getPicUrl()
