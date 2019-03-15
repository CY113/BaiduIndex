# coding = utf-8


# 需求图谱
import scrapy


class RelatedWordItem(scrapy.Item):
    keyword = scrapy.Field() # 关键词
    related_word = scrapy.Field() # 相关词
    count = scrapy.Field() # 相关词搜索指数
    date = scrapy.Field() # 日期



    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "INSERT INTO demand_map(related_word,count,keyword,date) VALUES (%s, %s, %s, %s)"
        params = (self['related_word'],self['count'],self['keyword'],self['date'],)
        return insert_sql, params

