import requests
import json
import os
import logging
from bs4 import BeautifulSoup


def get_pics(url, proxies=None):
    """
    [summary]

    Args:
        url ([type]): [description]
        proxies ([type], optional): [description]. Defaults to None.
    """
    try:
        if proxies is not None:
            logging.info("使用代理：" + str(proxies))
            r = requests.get(url, proxies=proxies)
        else:
            logging.info("不使用代理")
            r = requests.get(url)
        logging.info(f"HTTP状态码： {r.status_code}")
    except Exception as e:
        logging.error(e)
        return None
    # 开始下载
    pic_list = []
    count = 1
    soup = BeautifulSoup(r.text, 'html.parser')
    if not(os.path.exists(soup.title.string)):
        os.mkdir(soup.title.string)
        logging.info("创建目录："+soup.title.string)
    logging.info(soup.title.string)
    for pic_url in soup.find_all('img'):
        if not pic_url.get('src').startswith(r"https://"):
            logging.info(f"正在处理：{pic_url}")
            pic_url = "https://telegra.ph" + pic_url.get('src')
            logging.info(f"获得链接：{pic_url}")
        else:
            pic_url = pic_url.get('src')
            logging.info(f"获得链接：{pic_url}.get('src')")
        pic_list.append(pic_url)
    for pic in pic_list:
        logging.info(f"正在下载：{pic}")
        with open(soup.title.string+os.path.sep+str(count).zfill(3)+os.path.splitext(pic)[-1], 'wb') as file:
            if proxies is not None:
                file.write(requests.get(pic, proxies=proxies).content)
            else:
                file.write(requests.get(pic).content)
        logging.info("下载完成：" + str(count).zfill(3)+os.path.splitext(pic)[-1])
        count += 1
    logging.info(f"页面下载完毕，共计下载 {str(count)} 张图片")


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    url = input("请输入页面地址：")

    get_pics(url, proxies=proxies)
