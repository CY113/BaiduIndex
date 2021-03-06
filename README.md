# 百度指数
## 代码更新至新库：https://github.com/CY113/PythonSpider/tree/main/BaiduIndex
## 1.概述
&emsp;&emsp;通过对[百度指数](http://index.baidu.com/ "百度指数")的趋势研究、需求图谱和人群画像的数据抓取，分析目标关键词在不同时期真实的百度指数即热度。

## 2.项目结构
![](http://doc.intcolon.com/server/../Public/Uploads/2019-12-12/5df1edb6545ff.png)

## 3.抓取步骤
&emsp;&emsp;爬虫分为两部分。百度指数使用requests+json结构抓取，省份、城市等指数使用Scrapy框架抓取。
### 3.1 百度指数抓取
#### 启动目录：
1. start.py

#### 准备：
1. 修改关键词列表keywords_list，
2. 修改抓取时间范围start_date和end_date
3. 关键词列表可以从数据库中获取（get_key_from_mysql），也可以从Excel表中获取（get_key_from_excel）。可根据实际情况修改字段。
4. 如果手动修改关键词列表需注意：关键词列表中所有关键词必须小写(参数要求)，否则报错。
5. 目前抓取数据存储到mysql中（save_to_sql）。

### 3.2 省份、城市指数抓取
#### 启动目录：
1. main.py

#### 配置参数
&emsp;&emsp;在settings中配置抓取参数，其中：
##### 1.抓取起始时间与结束时间
START_DATE = "2019-01-01"
END_DATE = "2019-04-01"
##### 2.更改数据库配置信息
MYSQL_HOST = ""
MYSQL_DBNAME = ''  # 数据库名字
MYSQL_USER = ''  # 数据库账号
MYSQL_PASSWD = ''  # 数据库密码
MYSQL_PORT = 3306
##### 3.手动更新IP池
IP_Pool = [

]
##### 4.Cookie截止目前仍然可用，不用更改。

#### 抓取步骤：
##### 1.获取关键词
可手动添加或者从数据库中获取。

##### 2.抓取时间范围
&emsp;&emsp;默认根据settings中所设置开始和结束时间，分解成步长为月的时间列表；如果需要离散时间参数，可手动设置self.date_range_list

##### 3.更改各自item中的mysql插入语句
![](http://doc.intcolon.com/server/../Public/Uploads/2019-12-12/5df1f299500d8.png)
##### 4.启动爬虫

## 4.数据分析
#### 4.1 原理
&emsp;&emsp;对于省份和城市指数并不是真实热度，而是占比。最大值为1000,。那么可根据真实百度指数(每天)来计算在不同地域的关键词热度。
##### 计算方法：
1. 将某关键词在抓取时间段内，每一天的百度指数按月份相加求和,那么就获得每一个月改关键词在全国的百度指数和。
2. 计算各省份在指定时间段内在全国内热度百分比。用改关键词在该时间段内真实百度指数和相乘，即可得到该关键词的真实省份热度。
3. 城市计算方法和省份相同。计算城市在所属省份中的占比，然后乘以该省份真实热度。


#### 4.2 分析文件
百度指数数据处理.ipynb

