# coding=utf-8
from multiprocessing.pool import ThreadPool

from DBHelper import DBHelper
from get_index import BaiduIndex
import pandas as pd
import numpy as np


def main(keyword):
    baidu_index = BaiduIndex(keyword, '2018-01-01', '2019-01-01')
    data = baidu_index.result[keyword]['all']
    for i in range(len(data)):
        date = data[i]['date']
        index = data[i]['index']
        sql = "INSERT INTO baidu_index(keyword,_index,date) VALUES (%s, %s, %s)"
        params = (keyword, index, date)
        DBHelper().insert_task(sql, params)
if __name__ == "__main__":
    """
    从数据库中获取关键词列表
    """
    sql = 'SELECT DISTINCT(`描述关键词串`) from task3 where id > 136'
    keywords = DBHelper().query_task(sql)
    for keyword in keywords:
        baidu_index = BaiduIndex(str.lower(keyword[0]), '2018-01-01', '2019-01-01')
        data = baidu_index.result[str.lower(keyword[0])]['all']
        for i in range(len(data)):
            date = data[i]['date']
            index = data[i]['index']
            sql = "INSERT INTO baidu_index(keyword,_index,date) VALUES (%s, %s, %s)"
            params = (keyword,index,date)
            DBHelper().insert_task(sql,params)
