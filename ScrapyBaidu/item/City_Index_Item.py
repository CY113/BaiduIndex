# coding = utf-8


# 城市搜索指数
import scrapy


class CityIndexItem(scrapy.Item):
    keyword = scrapy.Field() # 关键词
    city = scrapy.Field() # 城市ID
    city_index = scrapy.Field() # 城市搜索指数
    prov = scrapy.Field() # 所属省份ID
    date = scrapy.Field() # 日期


    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "insert into city_index(keyword,city,city_index,prov,date) values(%s,%s,%s,%s,%s)"
        params = (self['keyword'],self['city'],self['city_index'],self['prov'],self['date'],)
        return insert_sql, params

