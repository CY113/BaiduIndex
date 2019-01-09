# coding=utf-8

"""

抓取关键词相关的需求图谱
严格按照百度指数上的时间段作为起始日期
"""
import datetime
from urllib.parse import quote
import requests
import json
from DBHelper import DBHelper

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'Cookie': "BAIDUID=D9EC96A2BCC8FE5180ECCE103DE9B287:FG=1; BIDUPSID=D9EC96A2BCC8FE5180ECCE103DE9B287; PSTM=1544279256; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=jhneTVqZ0tRNHJld0RxV1VuaXdkQXdMQ1NkbXJCVjM0WXpFNFg3R0NUM2FjMXBjQVFBQUFBJCQAAAAAAAAAAAEAAAAy9rZS6rvYrezhzOwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANrmMlza5jJcd; H_PS_PSSID=1438_21106_28205_28132_26350_28266_27244; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1546843709,1546848801,1546855885,1546927315; bdindexid=qi14jh2aju36phk6dbktdqtau7; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1546927428"
}


class DemandMap():
    def __init__(self, keyword, startdate, enddate):
        self._keywords = keyword
        self.date_range_list = self.get_time_range_list(startdate, enddate)
        self.url = "http://index.baidu.com/Interface/Newwordgraph?word={}&datelist=".format(
            quote(keyword))

    def get_data(self):
        """
        根据不同时间段获取响应 并存储数据库
        :return:
        """
        for date in self.date_range_list:
            start_url = self.url + str(date)
            response = requests.get(start_url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                data = json.loads(response.text)['data'][date]
                for i in range(len(data)):
                    word,count = data[i].split('\t')
                    sql = "INSERT INTO demand_map(related_word,count,keyword,date) VALUES (%s, %s, %s, %s)"
                    params = (word,count,self._keywords,date)
                    DBHelper().insert_task(sql,params)
            else:
                print('失败')
                print(start_url)


    def get_time_range_list(self, startdate, enddate):
        """
        获取时间参数列表，以七天为间隔
        :return: date_range_list
        """
        date_range_list = []
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        while 1:
            date_range_list.append(datetime.datetime.strftime(startdate, '%Y%m%d'))
            if startdate > enddate:
                date_range_list.pop()
                return date_range_list
            startdate = startdate + datetime.timedelta(days=7)


if __name__ == '__main__':
    DemandMap = DemandMap('劲霸','2018-06-03', '2018-12-30') # 时间按照百度指数上的日期，其他日期没有数据，间隔为周
    DemandMap.get_data()