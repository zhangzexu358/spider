from scrapy.cmdline import execute
from othermodual import siteutil
import redis
import os
from urllib.parse import quote
import logging

import datetime
from datetime import timedelta


redis1=redis.StrictRedis(host='127.0.0.1',port=6379,db=0)

all_website_key= redis1.keys('*')

site = "vgtime"

redis_key = "scrapy crawl "+site


#execute('scrapy crawl kaidiforum'.split(' '))

def deal_web_dupefilter(web_name):
    '''
    删除一个网站对应的dupefilter

    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':dupefilter')
    except Exception as e:
        print (e)

def deal_web_items(web_name):
    '''
    删除某个网站中的item
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':items')
    except Exception as e:
        print (e)

def deal_web_start_urls(web_name):
    '''
    删除某个网站的start_urls
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':spider:strat_urls')
    except Exception as e:
        print(e)

def deal_web_requests(web_name):
    '''
    删除某个网站的requests
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':requests')
    except Exception as e:
        print(e)

def clear_redis(one):

    deal_web_dupefilter(one)
    deal_web_items(one)
    deal_web_requests(one)
    deal_web_start_urls(one)

if __name__ == '__main__':
     sitebean = siteutil.get_site_info(site)
     clear_redis(site)
     index_url = sitebean.all_web_index
     if index_url is not None:
         if isinstance(index_url,list):
            for url in index_url:
                 redis1.lpush(site + ':spider:strat_urls', url)
         else:
            redis1.lpush(site + ':spider:strat_urls', index_url)
     key_index = sitebean.key_index
     if key_index is not None:
         key_param = sitebean.key_search_param_name
         key_words = sitebean.key_words
         if isinstance(key_words, list):
             if len(key_words) > 0:
                 for word in key_words:
                     new_index = key_index.format(
                            word)
                     redis1.lpush(site + ':spider:strat_urls', new_index)

     execute(redis_key.split(' '))



