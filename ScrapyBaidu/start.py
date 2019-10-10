# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.6.1
# @ Date: 2019/10/10 10:42
# @ Desc : 启动百度指数抓取

import numpy
import pandas as pd
from get_index import BaiduIndex
from tools.DBHelper import DBHelper


def get_key_from_excel(path, column_name):
    """
    从excel或csv中读取关键词列表,百度指数关键词默认小写
    :param path:  文件路径 -->str
    :param column_name: 关键词列列名 -->str
    :return: 关键词列表 --》list
    """
    keywords_list = []
    data = pd.read_excel(path)
    keywords = data[column_name].to_list()
    for keyword in keywords:
        keywords_list.append(str.lower(str(keyword)).strip())
    return keywords_list


def get_key_from_mysql(table_name):
    """
    从数据库中读取关键词列表,百度指数关键词默认小写
    :param table_name: 数据库表名 -->str
    :return: 关键词列表 --》list
    """
    keyword_list = []
    sql = 'SELECT DISTINCT(`keyword`) from {}'.format(table_name)
    from tools.DBHelper import DBHelper
    keywords = DBHelper().query_task(sql)
    for keyword in keywords:
        keyword_list.append(str.lower(str(keyword[0])).strip())
    keyword_list.sort()
    return keyword_list


def save_to_sql(params):
    """
    将数据存入mysql
    :param params: 由keyword, index, date组成的元组 --》tuple
    :return:
    """
    sql = "INSERT INTO baidu_index(keyword,_index, date) VALUES (%s, %s, %s)"
    DBHelper().insert_task(sql, params)


def main(keywords_list, start_date, end_date):
    """
    爬虫调用主程序
    :param keywords_list: 关键词列表 -->list
    :param start_date: 开始时间 -->str
    :param end_date: 结束时间 -->str
    :return: 存入数据库
    """
    for keyword in keywords_list:
        index = BaiduIndex(keyword, start_date, end_date)
        data = index.result[keyword]["all"]
        for i in range(len(data)):
            index = data[i]["index"]
            date = data[i]["date"]
            save_to_sql((keyword, index, date))


if __name__ == '__main__':
    path = "E:/github/BaiduIndex/ScrapyBaidu/tools/0719.xlsx"  # 文件位置
    column_name = "描述关键词串"  # 关键词列名
    keywords_list = get_key_from_excel(path, column_name)  # 获取关键词列表，此处从excel中提取
    start_date = "2019-01-01"
    end_date = "2019-01-31"
    main(keywords_list, start_date, end_date)  # 启动爬虫
