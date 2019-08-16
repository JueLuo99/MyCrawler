import os
import re
import requests
import time

# 下载路径，默认为该文件所在路径
downloadPath = os.path.abspath(os.path.dirname(__file__))
downloadPath += os.path.sep + time.strftime("%Y%m%d_%H%M%S", time.localtime())

# 创建工作空间
if not(os.path.exists(downloadPath)):
    os.mkdir(downloadPath)

def getPicURL(url):
    """
    获取图片的下载地址
    """
    # 访问图片的详情页
    response = requests.get(url)
    # 匹配出下载链接
    try:
        pattern = re.compile(r'<a id="image-resize-link" href="https://danbooru.donmai.us/data/[0-9a-z_\-]{0,}.(jpg|jpeg|png|bmp|gif)')
        picURL = str(pattern.search(response.text).group(0)).replace('<a id="image-resize-link" href="','')
    except AttributeError:
        # 部分图片体积不大，没有预览图，当前页面即为原图
        pattern = re.compile(r'src="https://danbooru.donmai.us/data/[0-9a-z_\-]{0,}.(jpg|jpeg|png|bmp|gif)')
        picURL = str(pattern.search(response.text).group(0)).replace('src="','')
    return picURL

def downloadPic(url):
    fileName = os.path.split(url)[1]
    with open(downloadPath+os.path.sep+fileName, 'wb') as file:
        file.write(requests.get(url).content)

response = requests.get("https://danbooru.donmai.us/posts?utf8=✓&tags=sayori")
# 匹配出当前页的每张图片的详情页并存入 idList
pattern = re.compile(r'<article id="post_[0-9]{0,}')
idList = pattern.findall(response.text)

# 转换为该页面每张图片的详情页
for i in range(len(idList)):
    idList[i] = idList[i].replace('<article id="post_','https://danbooru.donmai.us/posts/')

for i in idList:
    print("正在爬取 " + i + " 页面的原图")
    downloadURL = getPicURL(i)

    downloadPic(downloadURL)
    print("下载完毕 " + downloadURL)

# print(idList)


