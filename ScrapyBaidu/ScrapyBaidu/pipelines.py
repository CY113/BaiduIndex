# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings

from tools import DBHelper


class ScrapybaiduPipeline(object):
    def __init__(self):
        self.db_helper = DBHelper.DBHelper()

    def process_item(self, item, spider):
        try:
            sql, params = item.get_insert_sql()
            self.db_helper.insert_task(sql, params)
            print("插入数据库")
        except Exception as e:
            print(e)
