# WeiboSpider  

## 0. 效果展示  
* 0.1 爬取的POST的URL  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_urls.jpg)  
* 0.2 爬起的POST信息  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_posts.jpg)  
* 0.3 爬取的RESPONSE信息  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_responses.jpg)  

## 1. 软件下载  
* 1.1 微博模拟登录 selenium-3.11.0.tar.gz  
   tools文件下selenium-3.11.0.tar.gz  
* 1.2 浏览器模拟控制器 VCForPython27.rar和chromedriver_win32.zip  
  tools文件下VCForPython27.rar和chromedriver_win32.zip  
* 1.3 爬虫框架 Scrapy-1.5.0.tar.gz  
  tools文件下Scrapy-1.5.0.tar.gz  
* 1.4 mongo数据库下载  
  私人下载地址: 链接: <https://pan.baidu.com/s/141hIm59z7uuBse7r4K3-Kg> 密码: xj0h  
* 1.5 python2与数据库mongo的连接  
  tools文件下pymongo-3.6.1.tar.gz  
* 1.6 mongo数据库的可视化  
  tools文件下robomongo-0.9.0.rar  
 
## 2. 操作流程  
* 2.1 运行mongo数据库,创建本地地址localhost:27017  
双击mongodb文件下的start.bat  
* 2.2 下载post的URL链接(在spiders.py中填入用户ID号, 保证该项目运行一段时间)  
`cd WeiboSpiderUrls`  
`python start.py`  
* 2.3 下载post与response(在WeiboSpiderUrls项目启动一段时间后即可执行)  
`cd WeiboSpiderPosts`  
`python start.py`  
* 2.4 从数据库中导出文件并并清洗(需保证每一个ID号的post全部下载完成,正在进行...)  
`cd WeiboSpiderFilter`  
`python data_fetch.py`  

## 3. 下载

 
