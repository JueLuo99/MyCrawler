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


def getPicURL(url):
    """
    获取图片的下载地址
    """
    # 访问图片的详情页
    response = requests.get(url)
    # 匹配出原图的下载链接
    pattern = re.compile(r'<a id="image-resize-link" href="https://danbooru.donmai.us/data/[0-9a-z_\-]{0,}.(jpg|jpeg|png|bmp|gif)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0)).replace('<a id="image-resize-link" href="','')
        return picURL
    # 部分图片体积不大，没有预览图，当前页面即为原图
    pattern = re.compile(r'src="https://danbooru.donmai.us/data/[0-9a-z_\-]{0,}.(jpg|jpeg|png|bmp|gif)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0)).replace('src="','')
        return picURL   
    # 可能会出现格式为 webm 或 gif 甚至是 png 格式的动图（其他格式的也可能走这个域名）
    # 惊了，竟然还有 swf
    pattern = re.compile(r'https://raikou2.donmai.us/[0-9a-z_\-\/]{0,}.(webm|gif|png|jpg|jpeg|png|bmp|swf)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0))
        return picURL
    # 还有这个域名
    pattern = re.compile(r'https://raikou1.donmai.us/[0-9a-z_\-\/]{0,}.(webm|gif|png|jpg|jpeg|png|bmp|swf)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0))
        return picURL
    # 还有这个域名
    pattern = re.compile(r'https://cdn.donmai.us/original/[0-9a-z_\-\/]{0,}.(webm|gif|png|jpg|jpeg|png|bmp|swf)')
    if (pattern.search(response.text)):
        picURL = str(pattern.search(response.text).group(0))
        return picURL
    print("无法匹配图片下载链接")
    os.system("pause")
    raise Exception



def downloadPic(url):
    """
    保存目标图片
    """
    fileName = os.path.split(url)[1]
    # 如果已经存在就跳过
    if os.path.exists(downloadPath+os.path.sep+fileName):
        print("文件重复")
        return
    with open(downloadPath+os.path.sep+fileName, 'wb') as file:
        file.write(requests.get(url).content)



def getPostList(url):
    """
    获取目标页面的每个 post 的 URL 并返回一个 list
    如果没有更多页面，返回的 list 的第一个元素将为 "NoMorePages!"
    """
    response = requests.get(url)
    # 匹配出当前页的每张图片的详情页并存入 idList
    pattern = re.compile(r'<article id="post_[0-9]{0,}')
    idList = pattern.findall(response.text)

    # 没有更多页面时将 list 的第一个元素设为 "NoMorePages!"
    if len(idList)==0:
        pattern = re.compile(r'<p>Nobody here but us chickens!</p>')
        if pattern.search(response.text).group(0):
            idList.append("NoMorePages!")
            

    # 转换为该页面每张图片的详情页
    for i in range(len(idList)):
        idList[i] = idList[i].replace('<article id="post_','https://danbooru.donmai.us/posts/')
    return idList


# 创建工作空间
if not(os.path.exists(downloadPath)):
    os.mkdir(downloadPath)
print("创建目录 "+downloadPath)

# 默认从第 1 页开始爬取
page = 1

while True:
    # 构造目标网址，准备开始爬取
    url = "https://danbooru.donmai.us/posts?" + tag + "page=" + str(page)
    print("生成列表 " + url)
    postList = getPostList(url)
    if postList[0]=="NoMorePages!":
        print("\n爬取完毕 已无更多页面，程序即将退出")
        exit(0)
    print("生成列表 " + "该页面共有 " + str(len(postList)) + " 张图片")
    
    # 开始爬取并下载图片
    for post in postList:
        print("正在爬取 " + post + " 页面的原图")
        downloadURL = getPicURL(post)
        print("开始下载 " + downloadURL)
        downloadPic(downloadURL)
        print("下载完毕 " + downloadURL)
    
    # 当前页面爬取完毕，开始准备爬取下一页
    page += 1
    print("\n切换页面 当前页面爬取完毕，开始爬取第" + str(page) + "页\n")
    
