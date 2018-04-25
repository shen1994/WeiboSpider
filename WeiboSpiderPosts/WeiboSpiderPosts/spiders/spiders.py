# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 16:23:34 2018

@author: shen1994
"""

import re
import pymongo
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request

import WeiboSpiderPosts.settings as settings
from WeiboSpiderPosts.items import PostsItem
from WeiboSpiderPosts.items import ResponsesItem

# 设置模式
# mode = 0 暂时运行一段时间，保证数据库有一定的数据量
# mode = 1 爬取用户的post和response文件
mode = 0

class Spider(CrawlSpider):
    name = "WeiboSpiderPosts"
    host = "https://weibo.cn"

    start_urls = [
        1420174783, 1246792191, #1559383255, 1488403267, 1496878501,
        #1652707015, 1767505547, 1810510770, 1465005545, 1413578930,
        #1294355705, 1253268747, 1220824437, 2091080851, 1764535072,
        #1215163207, 1496970215, 1997074277, 1237145772, 1497511602,
        #1622749134, 1408106101, 1653261600, 1312429562, 1312429562,
        #1428141323, 1649970883, 1571343005, 1645847452, 1648811647,
    ]
    
    def start_requests(self):
	
        # 连接数据库
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        db = client[settings.MONGO_DB]
        url_collections = db["urls"]
		
        while(True):
            
            CHECK_TIMES = 5 # 遍历数据库5次全为空,退出当前所有操作
            should_stop = False
            
            # 保证从数据库中拿出数据
            user_ptr = 0
            user_number = len(self.start_urls)
            record_count = 0
            err_count = 0
            epoc_count = 0
        
            while(True):
                record_count = url_collections.find({"ID":str(self.start_urls[user_ptr])}).count()
                if record_count != 0:
                    err_count = 0
                    epoc_count = 0
                    break
                else:
                    err_count += 1
                    user_ptr += 1
                    if user_ptr >= user_number:
                        user_ptr = 0
                        
                if err_count >= user_number:
                    err_count = 0
                    epoc_count += 1
                    if epoc_count >= CHECK_TIMES:
                        should_stop = True
                        break
            
            if should_stop:
                break
            
            for i in range(record_count):
                url_dict = url_collections.find_one({"ID":str(self.start_urls[user_ptr])})
                _id = url_dict["_id"]
                ID = url_dict["ID"]
                comment_url = url_dict["comment_url"]
                transfer_url = url_dict["transfer_url"]
                url_collections.delete_one({"_id":_id, "ID":ID})
                yield Request(url=comment_url, meta={"_id":_id, "ID":ID}, callback=self.parse_posts) # post+comment
                yield Request(url=transfer_url, meta={"_id":_id, "ID":ID}, callback=self.parse_transfers) # transfer
        
    def parse_posts(self, response):
        """转发的评论内容的response"""
        
        # 提取html数据
        selector = Selector(response)
        post = selector.xpath(u'body/div[@class="c" and @id]/div/span[@class="ctt"]/text()').extract_first()
        time = selector.xpath(u'body/div[@class="c" and @id]/div/span[@class="ct"]/text()').extract_first()
        
        transfer = re.findall(u'\u8f6c\u53d1\[(\d+)\]', selector.xpath(u'body/div/span[1]/a/text()').extract_first())  # 转载数
        comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', selector.xpath(u'body/div/span[2]/text()').extract_first())  # 评论数
        like = re.findall(u'\u8d5e\[(\d+)\]', selector.xpath(u'body/div/span[3]/a/text()').extract_first())  # 点赞数
        
        # 装填进数据库
        post_item = PostsItem()
        
        post_item["_id"] = response.meta["_id"]
        post_item["ID"] = response.meta["ID"]
        if post:
            post_item["post"] = post
        if time:
            post_item["time"] = time
        if like:
            post_item["like"] = int(like[0])
        if transfer:
            post_item["transfer"] = int(transfer[0])
        if comment:
            post_item["comment"] = int(comment[0])
        
        yield post_item
        
        url_next = selector.xpath(u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], \
                          meta={"_id":response.meta["_id"], "ID": response.meta["ID"]}, callback=self.parse_comments)

    
    def parse_comments(self, response):
        """实际评论的内容的post"""
        selector = Selector(response)
        answers = selector.xpath(u'body/div[@class="c" and @id]')
        
        for answer in answers:
            answer_text = answer.xpath('span[@class="ctt"]/text()').extract_first()
            answer_id = answer.xpath('@id').extract_first()
            
            if answer_text and answer_id: # 确保comment不在记录里
                
                response_item = ResponsesItem()
                response_item["response"] = answer_text
                
                like = re.findall(u'\u8d5e\[(\d+)\]', answer.extract())  # 点赞数
                time = answer.xpath('span[@class="ct"]/text()').extract_first()
                
                response_item["_id"] = answer_id + response.meta["_id"] + response.meta["ID"]
                
                response_item["ID"] = response.meta["_id"]
                response_item["ID_ID"] = response.meta["ID"]

                if like:
                    response_item["like"]  = int(like[0])
                if time:
                    response_item["time"] = time
                    
                yield response_item
                
        url_next = selector.xpath(u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], \
                          meta={"_id":response.meta["_id"], "ID": response.meta["ID"]}, callback=self.parse_comments)
    
    def parse_transfers(self, response):
        """实际评论的内容的response"""
        selector = Selector(response)
        transfers = selector.xpath(u'body/div[@class="c"]')
        for transfer in transfers:
            like = re.findall(u'\u8d5e\[(\d+)\]', transfer.extract())  # 点赞数
            time = transfer.xpath(u'span[@class="ct"]/text()').extract_first()

            transfer_id = transfer.xpath(u'a[1]/@href').extract_first()
            
            if like and time and transfer_id: # 确保comment不在记录里
                
                response_item = ResponsesItem()
                response_item["like"]  = int(like[0])
                response_item["time"] = time
                
                response_item["_id"] = transfer_id + response.meta["_id"] + response.meta["ID"]
                
                response_item["ID"] = response.meta["_id"]
                response_item["ID_ID"] = response.meta["ID"]
                
                transfer_text = transfer.xpath('text()').extract_first()
                
                if transfer_text:
                    response_item["response"] = transfer_text
                    
                yield response_item
                
        url_next = selector.xpath(u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], \
                          meta={"_id":response.meta["_id"], "ID": response.meta["ID"]}, callback=self.parse_transfers)          
            