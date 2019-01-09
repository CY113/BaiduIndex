# coding=utf-8
"""
根据关键词抓取人群属性，包括年龄分布和性别分布

"""
import json
from urllib.parse import quote
import requests
from DBHelper import DBHelper

# 固定时间段为1个月，手动更改日期段列表
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
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    'Cookie': "BAIDUID=D9EC96A2BCC8FE5180ECCE103DE9B287:FG=1; BIDUPSID=D9EC96A2BCC8FE5180ECCE103DE9B287; PSTM=1544279256; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; indexpro=dtq3tjiq7v1kgc6shtasm2cr46; BDUSS=09XUEpZSDFyZ053dThHTG10MENZbERuSGZCQlJHV0hIdE03aVUzY1VuVWY5VnRjQVFBQUFBJCQAAAAAAAAAAAEAAADv27jpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB9oNFwfaDRcS; CHKFORREG=545275368d76f03b5fa3504aa5c4f132; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1546927315,1546938382,1546943550,1546998538; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1547005322; H_PS_PSSID=1438_21106_28132_26350_28266_27244; delPer=0; PSINO=2"
}


class CrowdProperty():
    def __init__(self, keyword):
        self.url = "https://index.baidu.com/api/SocialApi/getSocial?wordlist%5B%5D={}&startdate={}&enddate={}".format(
            quote(keyword), {}, {})

    def get_data(self):
        """
        根据不同时间段获取响应 并存储数据库
        :return:
        """
        for date in date_range_list:
            start_url = self.url.format(date[0], date[1])
            response = requests.get(url=start_url, headers=headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                data = json.loads(response.text)['data'][0]
                keyword = data['word']
                level1 = data['str_age']['1']
                level2 = data['str_age']['2']
                level3 = data['str_age']['3']
                level4 = data['str_age']['4']
                level5 = data['str_age']['5']
                male = data['str_sex']['M']
                female = data['str_sex']['F']
                self.insert(keyword,level1,level2,level3,level4,level5,male,female,str(date))
            else:
                print('失败')
                print(start_url)

    def insert(self,keyword,level1,level2,level3,level4,level5,male,female,date):
        sql = "insert into crowd_property(keyword,level1,level2,level3,level4,level5,male,female,date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (keyword,level1,level2,level3,level4,level5,male,female,date)
        DBHelper().insert_task(sql,params)

if __name__ == '__main__':
    CrowdProperty = CrowdProperty('胡歌')
    CrowdProperty.get_data()