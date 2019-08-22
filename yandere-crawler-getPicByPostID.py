import os
import re
import requests
import time

# 下载路径，默认为该文件所在路径
downloadPath = os.path.abspath(os.path.dirname(__file__))
downloadPath += os.path.sep + time.strftime("%Y%m%d", time.localtime())

# 需要爬取的图片的 Post ID ， 默认为空
postid = ""
print("请输入想要爬取的 Post ID：")
postid = input()
if not(postid):
    print("未输入 Post ID，程序即将退出")
    os.system("pause")
    exit()


def getPicURL(url):
    """
    获取图片的下载地址
    """
    # 访问图片的详情页
    response = requests.get(url)
    # 匹配出原图的下载链接
    pattern = re.compile(r'<a class="original-file-changed" id="highres" href="https://files.yande.re/image/.*.(jpg|jpeg|png|bmp|gif)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0)).replace('<a class="original-file-changed" id="highres" href="','')
        return picURL
    # 匹配格式为 PNG 的原图
    pattern = re.compile(r'<a class="original-file-unchanged" id="png" href=".*.(jpg|jpeg|png|bmp|gif)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0)).replace('<a class="original-file-unchanged" id="png" href="','')
        return picURL 
    print("无法匹配图片下载链接")
    os.system("pause")
    raise Exception



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


# 构造目标网址，准备开始爬取
url = "https://yande.re/post/show/" + postid


print("正在爬取 " + postid + " 页面的原图")
downloadURL = getPicURL(url)
print("开始下载 " + downloadURL)
downloadPic(downloadURL)
print("下载完毕 " + downloadURL)    