# coding=utf-8
from multiprocessing.pool import ThreadPool
from get_index import BaiduIndex
from tools.DBHelper import DBHelper

if __name__ == "__main__":
    """
    从数据库中获取关键词列表
    """
    sql = 'SELECT DISTINCT(`keyword`) from keyword_new'
    keywords = DBHelper().query_task(sql)
    for keyword in keywords: #keyword 是元组格式
        baidu_index = BaiduIndex(str.lower(keyword[0]).strip(), '2018-01-01', '2019-01-01') #百度自动将所有搜索词转为小写，数据库可能存取是有空格，去除掉
        data = baidu_index.result[str.lower(keyword[0]).strip()]['all']
        for i in range(len(data)):
            date = data[i]['date']
            index = data[i]['index']
            sql = "INSERT INTO baidu_index(keyword,_index,date) VALUES (%s, %s, %s)"
            params = (keyword,index,date)
            DBHelper().insert_task(sql,params)
