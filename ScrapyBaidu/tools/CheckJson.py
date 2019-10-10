# coding=utf-8
# @ Author: TianHao
# @ Python: Python3.6.1
# @ Date: 2018/03/10 16:21
# @ Desc : 判断是否符合Json格式
import json


def check_json_format(raw_msg):
    """
    判断是否符合Json格式
    :param self: data
    :return: 布尔值
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False
