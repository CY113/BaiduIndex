# -*- coding: utf-8 -*-
import calendar
import datetime
import json
import random
import scrapy
from scrapy.utils.project import get_project_settings

from ScrapyBaidu.settings import COOKIES
from item.City_Index_Item import CityIndexItem
from tools.QueryData import QueryData


class CityIndexSpider(scrapy.Spider):
    name = 'city_index'

    def __init__(self, *args, **kwargs):
        super(CityIndexSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self.base_url = 'https://index.baidu.com/api/SearchApi/region?region={}&word={}&startDate={}&endDate={}&days="'
        self.region_id = QueryData().get_region_id()
        # self.keywords = QueryData().get_keyword()
        self.keywords = ["爱奇艺"]
        self.date_range_list = self.get_time_range_list(self.settings["START_DATE"],
                                                        self.settings["END_DATE"])

    # def get_time_range_list(self, startdate, enddate):
    #     """
    #     获取时间参数列表，以三十天为间隔
    #     :return: date_range_list
    #     """
    #     date_range_list = []
    #     startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    #     enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    #     while 1:
    #         next_date = startdate + datetime.timedelta(days=7)
    #         if next_date < enddate:
    #             date_range_list.append((datetime.datetime.strftime(startdate,
    #                                                                '%Y-%m-%d'),
    #                                     datetime.datetime.strftime(next_date,
    #                                                                '%Y-%m-%d')))
    #             startdate = next_date
    #         else:
    #             return date_range_list
    def get_time_range_list(self,startdate, enddate):
        """
        获取时间参数列表，按月计算
        :param startdate: 起始时间 --> str
        :param enddate: 结束时间 --> str
        :return: date_range_list -->list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            next_month = startdate + datetime.timedelta(days=calendar.monthrange(startdate.year, startdate.month)[1])
            month_end = next_month - datetime.timedelta(days=1)
            if month_end < enddate:
                date_range_list.append((datetime.datetime.strftime(startdate,
                                                                   '%Y-%m-%d'),
                                        datetime.datetime.strftime(month_end,
                                                                   '%Y-%m-%d')))

    def start_requests(self):
        for keyword in self.keywords:
            for region_id in self.region_id:
                for date in self.date_range_list:
                    start_url = self.base_url.format(region_id[0], keyword, date[0], date[1])
                    yield scrapy.Request(url=start_url, callback=self.parse,
                                         cookies=random.choice(COOKIES),
                                         meta={'region': region_id[0]})

    def parse(self, response):
        result = json.loads(response.body.decode('utf-8'))
        if result['status'] != 10002:
            item = CityIndexItem()
            if result['data']:
                item['keyword'] = result['data']['region'][0]['key']
                item['prov'] = response.meta['region']
                item['date'] = result['data']['region'][0]['period']
                city = result['data']['region'][0]['city']
                for key, value in city.items():
                    item['city'] = key
                    item['city_index'] = value
                    yield item
            else:
                print(result['data']['region'][0]['key'] + "该地区数据为空")
        else:
            print("未收录该关键词")
