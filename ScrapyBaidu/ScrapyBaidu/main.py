# coding=utf-8

from scrapy import cmdline
cmdline.execute('scrapy crawl prov_index'.split()) # 抓取省份搜索指数
# cmdline.execute('scrapy crawl city_index'.split()) # 抓取市级搜索指数
# cmdline.execute('scrapy crawl related_word'.split()) # 抓取需求图谱中的相关词抓取
# cmdline.execute('scrapy crawl sex_age'.split()) # 抓取年龄占比和性别占比
