# coding = utf-8
"""
抓取关键词相关的需求图谱
严格按照百度指数上的时间段作为起始日期

"""
import datetime
import json
import random
from urllib.parse import quote
import scrapy
from ScrapyBaidu.settings import COOKIES
from item.Related_Word_Item import RelatedWordItem
from tools.QueryData import QueryData


class RelatedWordSpider(scrapy.Spider):
    name = 'related_word'

    def __init__(self, *args, **kwargs):
        super(RelatedWordSpider, self).__init__(*args, **kwargs)
        self.base_url = 'http://index.baidu.com/Interface/Newwordgraph?word={}&datelist='
        # self.keywords = QueryData().get_keyword()
        self.keywords = [("lol",),]
        self.date_range_list = self.get_time_range_list('2018-12-02','2018-12-30')

    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以七天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            date_range_list.append(
                datetime.datetime.strftime(startdate, '%Y%m%d'))
            if startdate > enddate:
                date_range_list.pop()
                return date_range_list
            startdate = startdate + datetime.timedelta(days=7)

    def start_requests(self):
        for keyword in self.keywords:
            for date in self.date_range_list:
                start_url = self.base_url.format(quote(keyword[0])) + str(date)
                yield scrapy.Request(url=start_url, callback=self.parse,
                                     cookies=random.choice(COOKIES),meta={'date':date})

    def parse(self, response):
        result = json.loads(response.body.decode('utf-8'))
        item = RelatedWordItem()
        date = response.meta['date']
        if result['status'] != 10002:
            if result['data']:
                item['keyword'] = result['0']
                item['date'] = date
                datas = result['data'][date]
                for i in range(len(datas)):
                    item['related_word'], item['count'] = datas[i].split('\t')
                    yield item
            else:
                print("该关键词暂无数据")

        else:
            print("未收录该关键词")

