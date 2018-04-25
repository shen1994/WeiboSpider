# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

import settings
from items import UrlsItem
from items import FollowsItem
from items import FansItem

class MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        db = client[settings.MONGO_DB]
        
        self.urls = db["urls"]
        self.follows = db["follows"]
        self.fans = db["fans"]
        
    def process_item(self, item, spider):
        
        if isinstance(item, UrlsItem):
            try:
                self.urls.insert(dict(item))
            except Exception:
                pass
            
        elif isinstance(item, FollowsItem):
            follows_items = dict(item)
            follows = follows_items.pop("follows")
            for i in range(len(follows)):
                follows_items[str(i + 1)] = follows[i]
            try:
                self.follows.insert(follows_items)
            except Exception:
                pass
            
        elif isinstance(item, FansItem):
            fans_items = dict(item)
            fans = fans_items.pop("fans")
            for i in range(len(fans)):
                fans_items[str(i + 1)] = fans[i]
            try:
                self.fans.insert(fans_items)
            except Exception:
                pass
            
        else:
            pass
        
        return item
