# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 16:23:34 2018

@author: shen1994
"""

import re
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

from WeiboSpiderUrls.items import UrlsItem
from WeiboSpiderUrls.items import FollowsItem
from WeiboSpiderUrls.items import FansItem

class Spider(CrawlSpider):
    name = "WeiboSpiderUrls"
    host = "https://weibo.cn"

    start_urls = [
        1420174783, 1246792191, #1559383255, 1488403267, 1496878501,
        #1652707015, 1767505547, 1810510770, 1465005545, 1413578930,
        #1294355705, 1253268747, 1220824437, 2091080851, 1764535072,
        #1215163207, 1496970215, 1997074277, 1237145772, 1497511602,
        #1622749134, 1408106101, 1653261600, 1312429562, 1312429562,
        #1428141323, 1649970883, 1571343005, 1645847452, 1648811647,
    ]
    
    scrawl_ID = set(start_urls)  # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID
    
    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)  # 加入已爬队列
            ID = str(ID)
            
            user_urls = "http://weibo.cn/%s/profile?filter=1&page=1" % ID
            yield Request(url=user_urls, meta={"ID":ID}, callback=self.parse_urls)
        
    def parse_urls(self, response):
        """ 抓取微博数据 """
        selector = Selector(response)
        tweets = selector.xpath(u'body/div[@class="c" and @id]')

        for tweet in tweets:
            
            urlsItems = UrlsItem() 
            content_id = tweet.xpath('@id').extract_first()
            urlsItems["_id"] = content_id # 保证唯一性
            urlsItems["ID"] = response.meta["ID"]
            
            url_comment = tweet.xpath(u'div/a[@class="cc"]/@href').extract()
            url_transfer = tweet.xpath(u'div/a[contains(text(),"\u8f6c\u53d1")]/@href').extract()
            
            if url_comment:
                urlsItems["comment_url"] = url_comment[0]
            if url_transfer:
                urlsItems["transfer_url"] = url_transfer[0]
                
            yield urlsItems        
        url_next = selector.xpath(u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], \
                          meta={"ID": response.meta["ID"]}, callback=self.parse_urls)
        
    def parse_fans_or_follows(self, response):
        """ 抓取关注或粉丝 """
        items = response.meta["item"]
        selector = Selector(response)
        # u"\u5173\u6ce8\u4ed6"--->关注他
        # u"\u5173\u6ce8\u5979"--->关注她
        text2 = selector.xpath(
            u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                response.meta["result"].append(elem[0])
                ID = int(elem[0])
                if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                    self.scrawl_ID.add(ID)
        # u"\u4e0b\u9875"--->下页          
        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()

        if url_next:
            yield Request(url=self.host + url_next[0], \
                          meta={"item": items, "result": response.meta["result"]}, \
                          callback=self.parse1)
        else:
            yield items 
            