# -*- coding: utf-8 -*-
import calendar
import datetime
import json
import random
import scrapy
from scrapy.utils.project import get_project_settings
from ScrapyBaidu.settings import COOKIES
from item.Prov_Index_Item import ProvIndexItem
from tools.QueryData import QueryData


class ProvIndexSpider(scrapy.Spider):
    name = 'prov_index'

    def __init__(self, *args, **kwargs):
        super(ProvIndexSpider, self).__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self.base_url = 'https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days="'
        # self.keywords = QueryData().get_keyword()
        self.keywords = ["福睿斯","宝来","宝骏560","朗动","宝骏510","大众波罗","博越","威朗","荣威RX5","逍客","凌渡","思域","昂克赛拉","风光580","瑞风S3","领动","比亚迪F3","飞度","威驰","科沃兹","帝豪GS","迈锐宝","起亚K2","艾瑞泽5","凌派","翼虎","赛欧","哈弗H6 Coupe","五菱宏光S1","途观L","凯美瑞","君越","欧尚","远景SUV","自由光","标致408","菱智","长安cx70","宝骏310","猎豹CS10","宝马X1","比亚迪宋","锋范","海马S5","爱丽舍","幻速S3","荣威360","众泰t600","帝豪GL","昕锐","长安CS15","标致308","启辰T70","凯越","东南dx7","朗行","日产阳光","雅力士","吉利金刚","骐达","昂科拉","标致301","中华V3","东南dx3","悦翔V7","马自达CX-4","风神AX7","绅宝X35","风光370","雪铁龙C3-XR","大迈X5","传祺GS8","森雅R7","欧蓝德","凯迪拉克XT5","风光330","凯迪拉克ATS","马自达6阿特兹","冠道","绅宝X25","景逸X5","宝骏310W","起亚KX3","幻速H3","杰德","博瑞","锐腾","起亚KX5","发现神行","瑞风M3","翼搏","哈弗H1","哥瑞","指南者","劲炫","陆风X7","途安","长安CS55","艾力绅","标致3008"]
        self.date_range_list = self.get_time_range_list(self.settings["START_DATE"],
                                                        self.settings["END_DATE"])

    # def get_time_range_list(self, startdate, enddate):
    #     """
    #     获取时间参数列表，以三十天为间隔
    #     :param startdate: 起始时间 --> str
    #     :param enddate: 结束时间 --> str
    #     :return: date_range_list -->list
    #     """
    #     date_range_list = []
    #     startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    #     enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    #     while 1:
    #         next_date = startdate + datetime.timedelta(days=30)
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
                startdate = next_month
            else:
                return date_range_list

    def start_requests(self):
        for keyword in self.keywords:
            for date in self.date_range_list:
                start_url = self.base_url.format(keyword, date[0], date[1])
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

