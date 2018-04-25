# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:15:10 2018

@author: shen1994
"""

import time
import json
import random
import StringIO
from math import sqrt
from PIL import Image
from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains

from ims import ims

weibo_accounts = [
    #{"username":'15238568085', "password":'hb727745'},
    {"username":'18280984615', "password":'hb999129'},
    #{"username":'13526194134', "password":'hb953454'},
]

PIXELS = []

def get_exact_type(image):
    '''
    实现精确剪裁
    '''
    imin = -1 # 一开始扫不到，行方向上记录一个头
    imax = -1 # 一直扫到图标不存在的地方
    jmin = -1
    jmax = -1
    
    row = image.size[0]
    col = image.size[1]
    
    for i in range(row):
        for j in range(col):
            if image.load()[i, j] != 255:
                imax = i
                break
            if imax == -1:
                imin = i
                
    for j in range(col):
        for i in range(row):
            if image.load()[i, j] != 255:
                jmax = j
                break
            if jmax == -1:
                jmin = j
                
    return (imin, jmin, imax + 1, jmax + 1)
    

def get_type(browser):
    '''
    识别图片路径
    '''
    image_type = ''
    img0 = Image.open(StringIO.StringIO(browser.get_screenshot_as_png()))
    box = browser.find_element_by_id('patternCaptchaHolder')
    img = img0.crop((int(box.location['x']) + 10, \
                     int(box.location['y']) + 100, \
                     int(box.location['x']) + box.size['width'] - 10, \
                     int(box.location['y']) + box.size['height'] - 10)).convert('L')
    
    new_box = get_exact_type(img)
    img = img.crop(new_box)
    width = img.size[0]
    height = img.size[1]

    for png in ims.keys():
        is_go_on = True
        
        for i in range(width):
            for j in range(height):
                # 大于245为空白，小于245为线条
                # 两个像素之间的差大于10，是为了去除245边界上的误差
                if ((img.load()[i, j] >= 245 and ims[png][i][j] < 245) or (img.load()[i, j] < 245 and ims[png][i][j] >= 245)) \
                        and abs(img.load()[i, j] - ims[png][i][j]) > 10:
                   is_go_on = False
                   break
            if not is_go_on:
                image_type = ''
                break
            else:
                image_type = png
                    
        if image_type.strip():
            break
    
    pix_x = box.location['x'] + 40 + new_box[0]
    pix_y = box.location['y'] + 130 + new_box[1]
    PIXELS.append((pix_x, pix_y))
    PIXELS.append((pix_x + 100, pix_y))
    PIXELS.append((pix_x, pix_y + 100))
    PIXELS.append((pix_x + 100, pix_y + 100))
    
    return image_type

def move(browser, coordinate_0, coordinate_1):
    length = sqrt((coordinate_1[0] - coordinate_0[0]) ** 2 + (coordinate_1[1] - coordinate_0[1]) ** 2)
    
    if length < 3:
        ActionChains(browser).move_by_offset(coordinate_1[0] - coordinate_0[0], \
                    coordinate_1[1] - coordinate_0[1]).perform()
        return
    else:
        step = random.randint(2, 4)
        x = int(step * (coordinate_1[0] - coordinate_0[0]) / length)
        y = int(step * (coordinate_1[1] - coordinate_0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, (coordinate_0[0] + x, coordinate_0[1] + y), coordinate_1)
    
def finger_draw(browser, image_type):
    if len(image_type) == 4:
        act_0 = PIXELS[int(image_type[0]) - 1]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_to_element(login).move_by_offset( \
                act_0[0] - login.location['x'] - int(login.size['width'] / 2), 
                act_0[1] - login.location['y'] - int(login.size['height'] / 2)).perform()
        browser.execute(Command.MOUSE_DOWN, {})
        
        act_1 = PIXELS[int(image_type[1]) - 1]
        move(browser, act_0, act_1)
        
        act_2 = PIXELS[int(image_type[2]) - 1]
        move(browser, act_1, act_2)

        act_3 = PIXELS[int(image_type[3]) - 1]
        move(browser, act_2, act_3)

        browser.execute(Command.MOUSE_UP, {})
    else:
        print 'Sorry! Failed! Maybe you need to update the code.'
       
def get_cookie_from_weibo(username, password):
    weibo_browser = webdriver.Chrome()
    try:
        weibo_browser.set_window_size(1050, 840)
        weibo_browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/')
        
        time.sleep(1)
        
        name = weibo_browser.find_element_by_id('loginName')
        psw = weibo_browser.find_element_by_id('loginPassword')
        login = weibo_browser.find_element_by_id('loginAction')
        name.send_keys(username)
        psw.send_keys(password)
        login.click()
        
        time.sleep(3.5)
        
        image_type = get_type(weibo_browser)
        finger_draw(weibo_browser, image_type)
        
        while "我的首页".decode("utf-8") not in weibo_browser.title:
            time.sleep(3)
        
        if "未激活微博".decode("utf-8") in weibo_browser.page_source:
            print "账号未开通微博"
            
        cookie = {}
        if "我的首页".decode("utf-8") in weibo_browser.title:
            for elem in weibo_browser.get_cookies():
                cookie[elem["name"]] = elem["value"]
            return cookie
    except Exception, e:
        print "%s---%s---%s!" % (e, username, password)
    finally:
        weibo_browser.quit()
        
def get_cookies(accounts):
    cookies = []
    for elem in weibo_accounts:
        username = elem["username"]
        password = elem["password"]
        cookie = get_cookie_from_weibo(username, password)
        if cookie != None:
            cookies.append(cookie)
            
    return cookies
        
cookies = get_cookies(weibo_accounts)
   