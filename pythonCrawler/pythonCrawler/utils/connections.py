#coding:utf-8
__author__ = 'mwy'
__date__ = '2017/10/6 14:21'

from elasticsearch_dsl.connections import connections
import redis

es = connections.create_connection(es_jobType._doc_type.using)
redis_cli = redis.StrictRedis(host="localhost")