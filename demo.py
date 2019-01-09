from DBHelper import DBHelper
from get_index import BaiduIndex

if __name__ == "__main__":
    """
    最多一次请求5个关键词
    """
    keywords = ['腾讯','阿里巴巴','百度','华为','小米','苹果']
    for keyword in keywords:
        baidu_index = BaiduIndex(keyword, '2018-01-01', '2019-01-01')
        data = baidu_index.result[keyword]['all']
        for i in range(len(data)):
            date = data[i]['date']
            index = data[i]['index']
            sql = "INSERT INTO baidu_index(keyword,_index,date) VALUES (%s, %s, %s)"
            params = (keyword,index,date)
            DBHelper().insert_task(sql,params)
