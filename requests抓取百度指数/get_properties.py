# coding=utf-8
"""
根据关键词抓取人群属性，包括年龄分布和性别分布

"""
import json
import random
import time
from urllib.parse import quote
import requests
from requests抓取百度指数.DBHelper import DBHelper

# 固定时间段为1个月，手动更改日期段列表
from requests抓取百度指数.config import COOKIES

date_range_list = [
    (20180601, 20180701),
    (20180701, 20180801),
    (20180801, 20180901),
    (20180901, 20181001),
    (20181001, 20181101),
    (20181101, 20181201),
    (20181201, 20190101),
]

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}


class CrowdProperty():
    def __init__(self, keyword):
        self._keyword = keyword
        self.url = "https://index.baidu.com/api/SocialApi/getSocial?wordlist%5B%5D={}&startdate={}&enddate={}".format(
            quote(keyword), {}, {})

    def get_data(self):
        """
        根据不同时间段获取响应 并存储数据库
        :return:
        """
        for date in date_range_list:
            start_url = self.url.format(date[0], date[1])
            headers['Cookie'] = random.choice(COOKIES)
            response = requests.get(url=start_url, headers=headers)
            time.sleep(1)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                data = json.loads(response.text)['data'][0]
                if len(data) > 2:
                    keyword = data['word']
                    level1 = data['str_age']['1']
                    level2 = data['str_age']['2']
                    level3 = data['str_age']['3']
                    level4 = data['str_age']['4']
                    level5 = data['str_age']['5']
                    male = data['str_sex']['M']
                    female = data['str_sex']['F']
                    self.insert(keyword, level1, level2, level3, level4, level5,
                                male, female, str(date))
                else:
                    print('没有该关键词' + ":" + self._keyword)
                    break
            else:
                print('失败')
                print(start_url)

    def insert(self, keyword, level1, level2, level3, level4, level5, male,
               female, date):
        sql = "insert into crowd_property(keyword,level1,level2,level3,level4,level5,male,female,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        keyword, level1, level2, level3, level4, level5, male, female, date)
        DBHelper().insert_task(sql, params)


if __name__ == '__main__':
    sql = 'SELECT DISTINCT(`描述关键词串`) from task3'
    keywords = DBHelper().query_task(sql)
    for keyword in keywords:
        C = CrowdProperty(keyword[0])
        C.get_data()
