# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.5
# @ Date: 2018/03/10 12:23
# @ Desc : 数据库操作

import pymysql
from DBUtils.PooledDB import PooledDB
from scrapy.utils.project import get_project_settings


class DBHelper(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    def connect_database(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.passwd, db=self.db,
                               charset='utf8')
        # pool = PooledDB(pymysql, 20, host=self.host, user=self.user,
        #                 passwd=self.password, db=self.db, port=3306,
        #                 charset="utf8")  # 20为连接池里的最少连接数
        # conn = pool.connection()
        return conn

    def insert_task(self, sql, params):
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def query_task(self, sql, *params):
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def query_fetchone_task(self, sql, params):
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql, params)
        results = cur.fetchone()
        cur.close()
        conn.close()
        return results

    def update_task(self, sql, params):
        conn = self.connect_database()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()

    def delete_task(self, sql, params):
        conn = self.connect_database()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


if __name__ == "__main__":
    db = DBHelper()
    sql = "insert into test(keyword,city,city_index,prov,date) values(%s,%s,%s,%s,%s)"
    params = ("test", 1, 500, 999, "2019-01-21|2019-01-28")
    db.insert_task(sql, params)
