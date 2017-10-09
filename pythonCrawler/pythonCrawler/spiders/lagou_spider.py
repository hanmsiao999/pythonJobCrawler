#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/5 7:49'

import json

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from pythonCrawler.items import JobItem
from utils.util import long_text_join

class lagou_spider(CrawlSpider):
       name='lagou'
       allowed_domains = ['www.lagou.com']
       start_urls = ["https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0"]
       header = {
           "Host": "www.lagou.com",
           "Referer": "	https://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD",
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
       }

       def start_requests(self):
           for i in range(1,31):
               print ("start_url:",str(i))
               yield scrapy.FormRequest(
                   url=self.start_urls[0],
                   formdata={
                       'first':'true',
                       'kd':'Python',
                       'pn':str(i)
                   },
                   headers=self.header,
                   callback=self.parse,
               )


       def parse(self, response):
           try:
               data = json.loads(response.text)
               data = data['content']['positionResult']['result']
               for job_item in data:
                   positionId = job_item['positionId']
                   job = JobItem()
                   job['job_org'] = "拉勾网"
                   job['title'] = job_item['positionName']
                   job['companyName'] = job_item['companyFullName']
                   job['jobCity'] = job_item['city']
                   detail_url = "https://www.lagou.com/jobs/%s.html" % (str(positionId))
                   job['jobUrl'] = detail_url
                   job['salaryInfo'] = job_item['salary']
                   job['create_time'] = job_item['createTime']
                   yield Request(url=detail_url,meta={'job':job},headers=self.header,callback=self.parse_detail)
           except Exception as ex:
               print (ex)


       def parse_detail(self,response):
           job = response.meta['job']
           workAddress = response.xpath(".//div[@class='work_addr']//text()").extract()
           job['workAdress'] = long_text_join(workAddress)
           jobDesc = response.xpath(".//dd[@class='job_bt']//text()").extract()
           job['jobDesc'] = long_text_join(jobDesc)
           yield job
