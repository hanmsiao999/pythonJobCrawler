#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/5 8:52'

import re
from functools import reduce

def get_salary_mid(text):
    if not text:
        return '0'
    text = text.replace("k","000")
    text = text.replace("千", "000")
    text = text.replace("万", "0000")
    text = re.findall("\d+",text)
    text = list(map(lambda  x:int(x.strip()), text))
    return str(int(reduce(lambda x, y: x + y, text, 0) / len(list(text))))


def long_text_join(text):
    text = map(lambda x: x.strip(), text)
    text = "".join(list(filter(lambda x: len(x) > 1, text)))
    return text



import random, requests,time
class Random_ip(object):
       def __init__(self):
           self.ip_set = []

       def getIP(self):
           if len(self.ip_set) == 0:
               self.download_ip()
           ip = random.choice(self.ip_set)
           return ip

       def download_ip(self):
           url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=49595241242b4c7f80d36a119d37d245&orderno=YZ20175265966odSeF2&returnType=1&count=10"
           this_head = {
                          'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                          "Upgrade-Insecure-Requests": '1',
                       }
           resutls = requests.get(url)
           time.sleep(5)
           ips = self.load_ip(resutls)
           self.ip_set.extend(ips)

       def load_ip(self, resutls):
           ips = resutls.content.decode("utf-8").split("\n")
           ips = list(filter(lambda x:len(x)>0 , ips))
           ips = [item.strip() for item in ips]
           return ips

       def delete_ip(self,ip):
           if ip in self.ip_set:
               self.ip_set.remove(ip)
