# WeiboSpider 

## 0.效果展示  
* 爬取微博用户发布内容的评论和转发网址,作为爬取内容的接口  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_urls.jpg)  
* 爬取用户的发布内容  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_posts.jpg)  
* 爬取用户对该发布内容的所有评论和转发内容  
![image](https://github.com/shen1994/README/raw/master/images/WeiboSpider_responses.jpg)  

## 1.安装相关文件  
* tools文件下的selenium-3.11.0.tar.gz,html内容提取安装包  
* tools文件下的chromedriver_win32.zip,版本:V2.38,选装google浏览器,解压放置在执行目录下即可,这只是临时做法,最好将其放置在google浏览器执行文件中,然后把它的路径添加到环境变量中.  
下载链接:<http://chromedriver.storage.googleapis.com/index.html>  
* tools文件下的VCForPython27.rar,下载链接:<https://www.microsoft.com/en-us/download/details.aspx?id=44266>  
* tools文件下的Scrapy-1.5.0.tar.gz,爬虫框架,依赖的文件很多,包括VCForPython27.rar  
* tools文件下的mongodb-win32-x86_64-2008plus-ssl-3.6.4-signed.rar,mongo数据库(暂时删除,自行下载),下载链接:  
<https://www.mongodb.org/dl/win32/x86_64-2008plus-ssl?_ga=2.229434714.714907189.1524314812-1414923153.1524314812>  
* mongodb私人下载链接: 链接: <> 密码: 
* tools文件下的pymongo-3.6.1.tar.gz,管理个人的数据库  
* tools文件下的robomongo-0.9.0.rar,mongo数据库的可视化工具  

## 2.账号需求
淘宝搜店铺:账号素材生产基地 或 互联网账号营销中心,1.2元可以购买3个  
共享账号:  
1. 15238568085----hb727745
2. 18280984615----hb999129
3. 13526194134----hb953454  

## 3.详细操作  
* 运行数据库,打开mongo文件夹，双击运行mongodb文件下start.bat  
* 数据库启动在localhost:27017下  
---
* 运行项目WeiboSpiderUrls,运行一段时间,确保数据库中存在内容  
* 执行以下命令  
* `cd WeiboSpiderUrls`  
* `python start.py`  
---
* 运行项目WeiboSpiderPosts,不断从数据库中读取URL，并且下载POST和RESPONSE内容  
* 执行以下命令  
* `cd WeiboSpiderPosts`  
* `python start.py`  

## 4.分布式批处理  
* 在同一台电脑上执行两个项目文件，但是需要更改settings文件中的MONGO_DB的文件名,确保抓取数据在同一数据库库中  
* 由于一台电脑的处理能力有限,推荐使用多台电脑操作,但是在不同电脑中的账户名需要改变,即cookies.py文件中的weibo_accounts  

## 5. 部分参考链接  
* <https://github.com/LiuXingMing/SinaSpider>  

