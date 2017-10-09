#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/7 11:08'

import json
from urllib import parse

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from pythonCrawler.items import JobBoleArticleItem
from utils.util import long_text_join


class jobbole_spider(CrawlSpider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    headers = {
        'Host':'blog.jobbole.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }

    def start_requests(self):
        yield Request(url=self.start_urls[0],headers=self.headers,callback=self.parse)

    def parse(self, response):
        thumbs_a = response.xpath(".//div[@class='post-thumb']/a")
        # 获取每篇文章详情
        for thumb_a in thumbs_a:
            article = JobBoleArticleItem()
            url = thumb_a.xpath("@href").extract_first("")
            title = thumb_a.xpath("@title").extract_first("")
            article['url'] = url
            article['title'] = title
            article['article_org'] = "伯乐在线"
            yield Request(url=url, meta={'article': article},headers=self.headers,
                          callback=self.parse_detail)

        # 获取下一页 可以不停yield
        next_urls = response.xpath(".//a[@class='next page-numbers']/@href").extract_first("")
        if next_urls:
            yield Request(url=next_urls, headers=self.headers,callback=self.parse)


    def parse_detail(self,response):
        #create_date content
        article = response.meta['article']
        create_date = response.xpath(".//p[@class='entry-meta-hide-on-mobile']/text()").extract_first("").replace("·","").strip()
        article['create_date'] = create_date
        content = long_text_join(response.xpath(".//div[@class='entry']/*/text()").extract())
        article['content'] = content
        yield article






