# coding = utf-8


# 人群属性：性别分布和年龄分布
import scrapy


class SexAgeItem(scrapy.Item):
    keyword = scrapy.Field()  # 关键词
    level1 = scrapy.Field()  # age <= 19
    level2 = scrapy.Field()  # 20< age <29
    level3 = scrapy.Field()  # 30< age <39
    level4 = scrapy.Field()  # 40< age <49
    level5 = scrapy.Field()  # age >= 50
    male = scrapy.Field()  # 男性比例
    female = scrapy.Field()  # 女性比例
    date = scrapy.Field() # 日期

    # 数据库插入语句
    def get_insert_sql(self):
        insert_sql = "insert into crowd_property(keyword,level1,level2,level3,level4,level5,male,female,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        self['keyword'], self['level1'], self['level2'], self['level3'],
        self['level4'],self['level5'],self['male'],self['female'],self['date'])
        return insert_sql, params
