# -*- coding: utf-8 -*-
import datetime
import json
import random

import scrapy

from ScrapyBaidu.settings import COOKIES
from item.Prov_Index_Item import ProvIndexItem
from tools.QueryData import QueryData


class ProvIndexSpider(scrapy.Spider):
    name = 'prov_index'

    def __init__(self, *args, **kwargs):
        super(ProvIndexSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days="'
        self.keywords = QueryData().get_keyword()
        self.date_range_list = self.get_time_range_list('2018-06-03',
                                                        '2018-12-30')

    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以三十天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            next_date = startdate + datetime.timedelta(days=7)
            if next_date < enddate:
                date_range_list.append((datetime.datetime.strftime(startdate,
                                                                   '%Y-%m-%d'),
                                        datetime.datetime.strftime(next_date,
                                                                   '%Y-%m-%d')))
                startdate = next_date
            else:
                return date_range_list

    def start_requests(self):
        for keyword in self.keywords:
            for date in self.date_range_list:
                start_url = self.base_url.format(str.lower(keyword[0]).strip(),
                                                 date[0], date[1])
                yield scrapy.Request(url=start_url, callback=self.parse,
                                     cookies=random.choice(COOKIES))

    def parse(self, response):
        result = json.loads(response.body.decode('utf-8'))
        if result['status'] != 10002:
            item = ProvIndexItem()
            if result['data']:
                item['keyword'] = result['data']['region'][0]['key']
                prov = result['data']['region'][0]['prov']
                item['date'] = result['data']['region'][0]['period']
                for key, value in prov.items():
                    item['prov'] = key
                    item['prov_index'] = value
                    yield item
            else:
                print(result['data']['region'][0]['key'] + "该地区数据为空")
        else:
            print("未收录该关键词")
