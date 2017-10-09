# coding:utf-8
__author__ = 'mwy'

from  scrapy.cmdline import execute
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy",'crawl',"lagou"])
#execute(["scrapy",'crawl',"wuyou"])
execute(["scrapy",'crawl',"jobbole"])
