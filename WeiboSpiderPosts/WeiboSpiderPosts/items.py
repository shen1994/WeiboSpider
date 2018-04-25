# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PostsItem(scrapy.Item):
    _id = scrapy.Field()
    ID = scrapy.Field()
    post = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    transfer = scrapy.Field()
    time = scrapy.Field()
    
class ResponsesItem(scrapy.Item):
    _id = scrapy.Field()
    ID = scrapy.Field()
    ID_ID = scrapy.Field()
    response = scrapy.Field()
    like = scrapy.Field()
    time = scrapy.Field()
