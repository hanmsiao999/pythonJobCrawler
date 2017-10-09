#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/5 11:56'




from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider

from utils.util import get_salary_mid, long_text_join
from pythonCrawler.items import JobItem

class wuyou_spider(RedisSpider):
    name = 'wuyou'
    allowed_domains = ['search.51job.com','jobs.51job.com']
    start_urls=['http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,%s.html']
    redis_key = "wuyou:start_urls"
    header = {
        "Host": "search.51job.com",
        "Upgrade-Insecure-Requests": "1",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    # def __init__(self):
    #     r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    #     r.set(self.redis_key, self.start_urls[0])


    def start_requests(self):
        yield Request(url=self.start_urls[0] % str(1),headers=self.header,callback=self.parse)

    def parse(self,response):
        # 解析商品
        jobs = response.xpath(".//*[@id='resultList']/div[@class='el']")
        count = 0
        for job_item in jobs:
            try:
                title = job_item.xpath(".//p[contains(@class,'t1')]/span/a/@title").extract_first().strip()
                jobUrl = job_item.xpath(".//p[contains(@class,'t1')]/span/a/@href").extract_first().strip()
                companyName = job_item.xpath(".//span[normalize-space(@class)='t2']/a/@title").extract_first().strip()
                jobCity = job_item.xpath(".//span[normalize-space(@class)='t3']/text()").extract_first().strip()
                salaryInfo = long_text_join(job_item.xpath(".//span[normalize-space(@class)='t4']/text()").extract())
                create_time = job_item.xpath(".//span[normalize-space(@class)='t5']/text()").extract_first().strip()
                job = JobItem()
                job['job_org'] = "前程无忧"
                job['title'] = title
                job['companyName'] = companyName
                job['jobCity'] = jobCity
                job['jobUrl'] = jobUrl
                job['salaryInfo'] = salaryInfo
                job['create_time'] = create_time
                count += 1

                yield Request(url=jobUrl,headers=self.header,meta={'job':job},callback=self.parse_detail)
            except Exception as ex:
                print (response.url)
                print (ex)
                print (str(count))
                print ("="*20)



        # 解析下一页
        next_url = response.xpath(".//li[@class='bk'][last()]/a/@href").extract_first()
        print ("next_url:",next_url)
        if next_url:
            yield Request(url=next_url, headers=self.header, callback=self.parse)


    def parse_detail(self,response):
        job = response.meta['job']
        desc = long_text_join(response.xpath(".//div[@class='bmsg job_msg inbox']//text()").extract())
        workaddress = long_text_join(response.xpath(".//p[@class='fp']/text()").extract())
        job['jobDesc'] = desc
        job['workAdress'] = workaddress
        yield job













