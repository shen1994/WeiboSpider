# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

import settings
from items import PostsItem
from items import ResponsesItem

class MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        db = client[settings.MONGO_DB]
        
        self.posts = db["posts"]
        self.responses = db["responses"]
        
    def process_item(self, item, spider):
        
        if isinstance(item, PostsItem):
            try:
                self.posts.insert(dict(item))
            except Exception:
                pass
            
        elif isinstance(item, ResponsesItem):
            try:
                self.responses.insert(dict(item))
            except Exception:
                pass
            
        else:
            pass
        
        return item
