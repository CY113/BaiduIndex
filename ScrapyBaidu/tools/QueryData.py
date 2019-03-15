# coding=utf-8

from tools import DBHelper


class QueryData(object):
    def __init__(self):
        self.db_helper = DBHelper.DBHelper()

    def get_region_id(self):
        # 查询省份ID
        query_sql = "SELECT id FROM province_id ORDER BY id"
        return self.db_helper.query_task(query_sql)

    def get_keyword(self):
        sql = 'SELECT 描述关键词串 FROM task6_child'
        keywords = self.db_helper.query_task(sql)
        return keywords


if __name__ == '__main__':
    keywords = QueryData().get_keyword()
    print(keywords)
    print(len(keywords))
