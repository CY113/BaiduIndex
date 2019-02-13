# coding=utf-8

"""

抓取关键词相关的需求图谱
严格按照百度指数上的时间段作为起始日期
"""
import datetime
import random
from urllib.parse import quote
import requests
import json
from DBHelper import DBHelper
from config import COOKIES, IP_Pool

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}


class DemandMap():
    def __init__(self, keyword, startdate, enddate):
        self._keywords = keyword
        self.date_range_list = self.get_time_range_list(startdate, enddate)
        self.url = "http://index.baidu.com/Interface/Newwordgraph?word={}&datelist=".format(
            quote(keyword))

    def get_data(self,cookies=random.choice(COOKIES)):
        """
        根据不同时间段获取响应 并存储数据库
        :return:
        """
        proxies = {
            "http": "http://182.99.219.56:4276",
        }
        for date in self.date_range_list:
            start_url = self.url + str(date)
            headers['Cookie'] = cookies
            response = requests.get(start_url, headers=headers,proxies = proxies)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                data = json.loads(response.text)
                if data['data'] != []:
                    datas = data['data'][date]
                    for i in range(len(datas)):
                        word,count = datas[i].split('\t')
                        sql = "INSERT INTO demand_map(related_word,count,keyword,date) VALUES (%s, %s, %s, %s)"
                        params = (word,count,self._keywords,date)
                        print('正在插入数据库')
                        DBHelper().insert_task(sql,params)
                else:
                    print('没有该关键词' + ":" + self._keywords)
                    break
            else:
                print('失败')
                print(start_url)


    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以七天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            date_range_list.append(datetime.datetime.strftime(startdate, '%Y%m%d'))
            if startdate > enddate:
                date_range_list.pop()
                return date_range_list
            startdate = startdate + datetime.timedelta(days=7)


if __name__ == '__main__':
    sql = 'SELECT DISTINCT(`描述关键词串`) from task3'
    keywords = DBHelper().query_task(sql)
    for keyword in keywords:
        D = DemandMap(keyword[0],'2018-12-02', '2018-12-30') # 时间按照百度指数上的日期，其他日期没有数据，间隔为周
        D.get_data()
