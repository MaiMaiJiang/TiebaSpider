#coding:utf-8
import os
import urllib
import urllib2
from lxml import etree

class Spider:
    def __init__(self):
        self.tiebaName = raw_input("请需要访问的贴吧：")
        self.beginPage = int(raw_input("请输入起始页："))
        self.endPage = int(raw_input("请输入终止页："))

        self.url = 'http://tieba.baidu.com/f'
        self.ua_header = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}


        self.userName = 1

    def tiebaSpider(self):
        for page in range(self.beginPage, self.endPage + 1):
            pn = (page - 1) * 50 # page number
            word = {'pn' : pn, 'kw': self.tiebaName}

            word = urllib.urlencode(word) #转换成url编码格式（字符串）
            myUrl = self.url + "?" + word

            # 并且获取页面所有帖子链接,
            links = self.loadPage(myUrl)

    # 读取页面内容
    def loadPage(self, url):
        req = urllib2.Request(url, headers = self.ua_header)
        html = urllib2.urlopen(req).read()

        # 解析html 为 HTML 文档
        selector=etree.HTML(html)


        links = selector.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')

        for link in links:
            link = "http://tieba.baidu.com" + link
            self.loadImages(link)

    # 获取图片
    def loadImages(self, link):
        req = urllib2.Request(link, headers = self.ua_header)
        html = urllib2.urlopen(req).read()

        selector = etree.HTML(html)

        imagesLinks = selector.xpath('//img[@class="BDE_Image"]/@src')

        for imagesLink in imagesLinks:
            self.writeImages(imagesLink)

    # 保存页面内容
    def writeImages(self, imagesLink):
        '''
            将 images 里的二进制内容存入到 userNname 文件中
        '''

        print imagesLink
        file = open('./images/' + str(self.userName)  + '.png', 'wb')
        images = urllib2.urlopen(imagesLink).read()

        file.write(images)

        file.close()

        self.userName += 1

if __name__ == "__main__":

    mySpider = Spider()

    mySpider.tiebaSpider()