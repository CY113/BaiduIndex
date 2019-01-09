# coding = utf-8
"""
抓取关键词搜索的地域分布
"""

import datetime
from urllib.parse import quote
import requests
import json

from DBHelper import DBHelper

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'Cookie': "BAIDUID=D9EC96A2BCC8FE5180ECCE103DE9B287:FG=1; BIDUPSID=D9EC96A2BCC8FE5180ECCE103DE9B287; PSTM=1544279256; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; bdindexid=qi14jh2aju36phk6dbktdqtau7; indexpro=dtq3tjiq7v1kgc6shtasm2cr46; BDUSS=09XUEpZSDFyZ053dThHTG10MENZbERuSGZCQlJHV0hIdE03aVUzY1VuVWY5VnRjQVFBQUFBJCQAAAAAAAAAAAEAAADv27jpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB9oNFwfaDRcS; CHKFORREG=545275368d76f03b5fa3504aa5c4f132; H_PS_PSSID=1438_21106_28205_28132_26350_28266_27244; delPer=0; PSINO=2; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1546855885,1546927315,1546938382,1546943550; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1546943554"
}


class Portrait():
    def __init__(self, keyword, startdate, enddate):
        self._keyword = keyword
        self.date_range_list = self.get_time_range_list(startdate, enddate)
        self.url = "https://index.baidu.com/api/SearchApi/region?region=0&word={}&startDate={}&endDate={}&days=".format(
            quote(keyword), {}, {})

    def get_data(self):
        for date in self.date_range_list:
            start_url = self.url.format(date[0], date[1])
            response = requests.get(start_url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.text)
                keyword = data['data']['region'][0]['key']
                prov = data['data']['region'][0]['prov']
                city = data['data']['region'][0]['city']
                self.insert_prov(keyword, prov, date)
                self.insert_city(keyword, city, date)
            else:
                print('失败')
                print(start_url)

    def insert_prov(self, keyword, prov, date):
        """
        将省份搜索指数存储数据库
        :param keyword: 关键词
        :param prov: 省份ID
        :param date: 日期
        :return:
        """
        for key, value in prov.items():
            sql = "insert into province_index(keyword,prov,prov_index,date) values(%s,%s,%s,%s) "
            params = (keyword, key, value, str(date))
            DBHelper().insert_task(sql, params)

    def insert_city(self, keyword, city, date):
        """
        将城市搜索指数存储数据库
        :param keyword: 关键词
        :param city: 城市ID
        :param date: 日期
        :return:
        """
        for key, value in city.items():
            sql = "insert into city_index(keyword,city,city_index,date) values(%s,%s,%s,%s)"
            params = (keyword, key, value, str(date))
            DBHelper().insert_task(sql, params)


    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以三十天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            next_date = startdate + datetime.timedelta(days=30)
            if next_date < enddate:
                date_range_list.append((datetime.datetime.strftime(startdate,
                                                                   '%Y-%m-%d'),
                                        datetime.datetime.strftime(next_date,
                                                                   '%Y-%m-%d')))
                startdate = next_date
            else:
                return date_range_list


if __name__ == '__main__':
    Portrait = Portrait('胡歌', '2018-06-03', '2018-12-30')
    Portrait.get_data()
