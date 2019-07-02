from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.request
import os
import img2pdf
import re


def GetPageByChrome(url):
    # 打开chrome浏览器（需提前安装好chromedriver）
    browser = webdriver.Chrome()
    # browser = webdriver.PhantomJS()
    print("正在打开网页...")
    browser.get(url)

    print("等待网页响应...")
    # 需要等一下，直到页面加载完成
    time.sleep(5)

    print("正在获取网页数据...")
    soup = BeautifulSoup(browser.page_source, "lxml")
    # pip install lxml if error

    browser.close()

    return soup


link = "https://wenku.baidu.com/view/253af8501fb91a37f111f18583d049649b660ee4.html?from=search"
output = r"D:\PYProjects\test"
soup = GetPageByChrome(link)
title = soup.find("span", id=re.compile("^doc-tittle-")).text
pages = soup.find_all("div", class_="ppt-image-wrap")
print("title={}, pages={}".format(title, len(pages)))
# title = "test"  # 如果文档名称有特殊符号，需要重新命名
if len(pages) > 0:
    if not os.path.exists(title):
        os.mkdir(title)
    print("正在下载图片...")
    i = 0
    imagelist = []
    for page in pages:
        i = i + 1
        print(i)
        if i <= 3:
            src = "src"
        else:
            src = "data-src"
        image = r'{0}\{1}\{2}.png'.format(output, title, i)
        imagelist.append(image)
        urllib.request.urlretrieve(page.img[src], image)
    print("创建pdf...")
    with open(r"{0}\{1}\{1}.pdf".format(output, title), "wb") as f:
        f.write(img2pdf.convert(imagelist))
else:
    print("未找到图片...")
print("结束")
