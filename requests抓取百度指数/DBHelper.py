# coding=utf-8
"""
数据库操作

"""

import pymysql


class DBHelper(object):
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = 'baiduindex'
        self.password = '123456'
        self.db = 'baiduindexdb'

    def connect_database(self):
        conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                               passwd=self.password, db=self.db,
                               charset='utf8')
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
    sql = """SELECT * FROM rent_review  WHERE house_code = %s AND time = %s """  # AND `time` = %s
    params = ('107001292240', '2018-07-05')
    print(db.query_task(sql, params))
