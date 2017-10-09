# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from elasticsearch_dsl.connections import connections
import redis

from models.es_jobType import es_jobType,ArticleType



es = connections.create_connection(es_jobType._doc_type.using)
redis_cli = redis.StrictRedis(host="182.254.155.33",password='wenyuan123')
def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text,weight in info_tuple:
        if text:
            # 调用es的 analyzer接口分析字符串
            words = es.indices.analyze(index=index,analyzer="ik_max_word",
                               params={"filter":["lowercase"]},body=text)
            anylyzed_words = set([r['token'] for r in words['tokens'] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input":list(new_words),"weight":weight})
    return suggests



class JobItem(scrapy.Item):
    title = scrapy.Field()
    companyName = scrapy.Field()
    workAdress = scrapy.Field()
    salaryInfo = scrapy.Field()
    jobDesc = scrapy.Field()
    jobCity = scrapy.Field()
    jobUrl = scrapy.Field()
    job_org = scrapy.Field()
    create_time = scrapy.Field()

    def save_to_es(self):
        job = es_jobType()
        job['title'] = self['title']
        job['companyName'] = self['companyName']
        job['workAdress'] = self['workAdress']
        job['jobDesc'] = self['jobDesc']
        job['jobCity'] = self['jobCity']
        job['jobUrl'] = self['jobUrl']
        job['job_org'] = self['job_org']
        job['salaryInfo'] = self['salaryInfo']
        job['create_time'] = self['create_time']
        job.suggest = gen_suggests(es_jobType._doc_type.index,((job.title,10),(job.jobDesc,7)))
        job.save()
        if self['job_org'] == '拉勾网':
           redis_cli.incr("lagouJobCount")
        if self['job_org'] == '前程无忧':
            redis_cli.incr("wuyouJobCount")


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    article_org = scrapy.Field()

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self['create_date']
        article.content = self['content']
        article.url = self['url']
        article.article_org = self['article_org']
        article.suggest = gen_suggests(ArticleType._doc_type.index,((article.title,10),))
        article.save()
        redis_cli.incr("jobbole_count")






