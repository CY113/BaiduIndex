# coding = utf-8
"""
抓取关键词搜索的地域分布
"""

import datetime
import random
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import quote
import requests
import json
import pandas as pd
import numpy as np
from DBHelper import DBHelper
from config import COOKIES, IP_Pool
import time

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}
proxies = {"http":random.choice(IP_Pool)}

class Portrait():
    def __init__(self, keyword, startdate, enddate):
        self._keyword = keyword
        self.date_range_list = self.get_time_range_list(startdate, enddate)
        self.url = "https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days=".format(
            quote(keyword), {}, {})

    def get_data(self):
        for date in self.date_range_list:
            start_url = self.url.format(date[0], date[1])
            headers['Cookie'] = random.choice(COOKIES)
            response = requests.get(start_url, headers=headers,proxies = {"http": random.choice(IP_Pool)})
            time.sleep(1)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data['data'] !='':
                    keyword = data['data']['region'][0]['key']
                    prov = data['data']['region'][0]['prov']
                    city = data['data']['region'][0]['city']
                    print('正在插入数据库')
                    self.insert_prov(keyword, prov, date)
                    self.insert_city(keyword, city, date)
                else:
                    print('没有该关键词' + ":" + self._keyword )
                    break
            else:
                print('失败')
                print(start_url)

    def insert_prov(self, keyword, prov, date):
        """
        将省份搜索指数存储数据库
        :param keyword: 关键词
        :param prov: 省份ID
        :param date: 日期
        :return:
        """
        try:
            for key, value in prov.items():
                sql = "insert into province_index(keyword,prov,prov_index,date) values(%s,%s,%s,%s) "
                params = (keyword, key, value, str(date))
                DBHelper().insert_task(sql, params)
        except Exception:
            print('数据为空')

    def insert_city(self, keyword, city, date):
        """
        将城市搜索指数存储数据库
        :param keyword: 关键词
        :param city: 城市ID
        :param date: 日期
        :return:
        """
        try:
            for key, value in city.items():
                sql = "insert into city_index(keyword,city,city_index,date) values(%s,%s,%s,%s)"
                params = (keyword, key, value, str(date))
                DBHelper().insert_task(sql, params)
        except Exception:
            print('数据为空')


    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以三十天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            next_date = startdate + datetime.timedelta(days=30)
            if next_date < enddate:
                date_range_list.append((datetime.datetime.strftime(startdate,
                                                                   '%Y-%m-%d'),
                                        datetime.datetime.strftime(next_date,
                                                                   '%Y-%m-%d')))
                startdate = next_date
            else:
                return date_range_list


if __name__ == '__main__':
    sql = 'SELECT DISTINCT(`描述关键词串`) from task3'
    keywords = DBHelper().query_task(sql)
    for keyword in keywords:
        P= Portrait(keyword[0], '2018-06-03', '2018-12-30')
        P.get_data()
