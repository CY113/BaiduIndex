import json
import random

from ScrapyBaidu.settings import IP_Pool
from tools.UserAgents import agents


class BaiduIndexUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = random.choice(agents)
        request.headers['User-Agent'] = ua


class BaiduIndexProxyMiddleware(object):
    def process_request(self, request, spider):
        ip = random.choice(IP_Pool)
        request.meta['proxy'] = ip
        print(request.meta['proxy'])

    def process_response(self, request, response, spider):
        if response.status == 200:
            result = json.loads(response.body.decode('utf-8'))
            if result['status'] == 0 or result['status'] == "0":
                return response
            elif result['status'] == 10000 or result['status'] == 10001:
                print("重新请求")
                ip = random.choice(IP_Pool)
                print("this is response ip:" + ip)
                request.meta['proxy'] = ip
                return request
            elif result['status'] == 10002:
                return response
            else:
                print("未知错误")
                ip = random.choice(IP_Pool)
                print("this is response ip:" + ip)
                request.meta['proxy'] = ip
                return request

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        ip = random.choice(IP_Pool)
        request.meta['proxy'] = ip
        return request

