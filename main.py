import re
import requests

response = requests.get("https://danbooru.donmai.us/posts?utf8=✓&tags=sayori")

pattern = re.compile(r'<article id="post_[0-9]{0,}')

idList = pattern.findall(response.text)

# 转换为该页面每张图片的详情页
for i in range(len(idList)):
    idList[i] = idList[i].replace('<article id="post_','https://danbooru.donmai.us/posts/')

    # https://danbooru.donmai.us/posts/3595525

print(idList)