# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

	
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UrlsItem(scrapy.Item):
    _id = scrapy.Field()
    ID = scrapy.Field()
    comment_url = scrapy.Field()
    transfer_url = scrapy.Field()

class FollowsItem(scrapy.Item):
    _id = scrapy.Field()
    follows = scrapy.Field()

class FansItem(scrapy.Item):
    _id = scrapy.Field()
    fans = scrapy.Field()

