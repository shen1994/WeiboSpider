# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from user_agents import agents
from cookies import cookies

class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        
class CookiesMiddleware(object):
    def process_request(self, request, spider):
        cookie = random.choice(cookies)
        request.cookies = cookie
