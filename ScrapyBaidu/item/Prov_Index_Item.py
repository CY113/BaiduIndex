# coding = utf-8


# 省份搜索指数
import scrapy


class ProvIndexItem(scrapy.Item):
    keyword = scrapy.Field() # 关键词
    prov = scrapy.Field() # 省份ID
    prov_index = scrapy.Field() # 省份搜索指数
    date = scrapy.Field() # 日期


    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "insert into province_index(keyword,prov,prov_index,date) values(%s,%s,%s,%s)"
        params = (self['keyword'],self['prov'],self['prov_index'],self['date'],)
        return insert_sql, params

