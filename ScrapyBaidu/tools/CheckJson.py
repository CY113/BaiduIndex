# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 15:51
# @Author  : Hunk
# @Email   : qiang.liu@ikooo.cn
# @File    : util.py.py
# @Software: PyCharm
import json


def check_json_format(raw_msg):
    """
    判断是否符合Json格式
    :param self:
    :return:
    """
    if isinstance(raw_msg, str):  # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False
