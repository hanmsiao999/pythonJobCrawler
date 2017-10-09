#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/5 9:26'



from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text,Integer

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class es_jobType(DocType):
    # 职位类型
    title = Text(analyzer='ik_max_word')
    suggest = Completion(analyzer=ik_analyzer)
    companyName = Text(analyzer='ik_max_word')
    workAdress = Keyword()
    salaryInfo = Keyword()
    jobDesc = Text(analyzer='ik_max_word')
    jobCity = Keyword()
    jobUrl = Keyword()
    job_org = Keyword()
    create_time = Keyword()


    class Meta:
        index = "jobdb"
        doc_type = "pythonjob"

class ArticleType(DocType):
    # 伯乐在线 文章类型
    title = Text(analyzer='ik_max_word')
    suggest = Completion(analyzer=ik_analyzer)
    create_date = Date()
    url = Keyword()
    content = Text(analyzer='ik_max_word')
    article_org = Keyword()

    class Meta:
        index = "jobdb"
        doc_type = "article_jobdb"


if __name__ == '__main__':
    #es_jobType.init()
    ArticleType.init()