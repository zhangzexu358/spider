# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from twisted.internet.defer import DeferredLock
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import time
import random
import requests
import os
import yaml
import json
import platform




class ScrapytestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class SeleniumMiddleware():
    USER_AGENT_LIST = [
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C)",
        # "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        #"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        #"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        #"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
        # "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
        # "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/44.0",
        #"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    ]


    def get_cookie(self, cookie_info):
        cookie_arr = cookie_info
        if len(cookie_arr) > 0:
            cookie = random.sample(cookie_arr, 1)
            return cookie[0]
        else:
            return None

    #为每个request请求带上header信息
    def process_request(self, request, spider):

        sitetype = spider.sitebean.sitetype
        if sitetype == 'jingwai':
            #request.headers['User-Agent'] = random.choice(self.USER_AGENT_LIST)
            request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        else:
            if spider.name=="vgtime":
                request.headers['User-Agent'] = 'okhttp/3.14.2'
            else:
                request.headers['User-Agent'] = random.choice(self.USER_AGENT_LIST)


#统一为请求带上代理信息
class HttpbinProxyMiddleware(object):
    WEIBO_USER_KEYWORD_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
    @classmethod
    def __init__(self):
        #self.helper = ProxyHelper()
        self.lock = DeferredLock()
        self.url_count = dict()
        self.lock_count = DeferredLock()

    def process_request(self, request, spider):
        sitetype = spider.sitebean.sitetype
        file_name = "address.yml"
        f = None

        if platform.system() == 'Linux':
            path = os.path.abspath('..')
            file_path = path + "/" + file_name
            try:
                f = open(file_path, "r", encoding='UTF-8')
            except Exception as e:
                path = os.path.abspath(os.curdir)
                file_path = path + "/spiderV1/" + file_name
                f = open(file_path, "r", encoding='UTF-8')
        else:
            path = os.path.abspath('..')
            file_path = path + "\\" + file_name
            try:
                f = open(file_path, "r", encoding='UTF-8')
            except Exception as e:
                path = os.path.abspath(os.curdir)
                file_path = path + "\\spiderV1\\" + file_name
                f = open(file_path, "r", encoding='UTF-8')

        temp = yaml.load(f.read())

        #外网代理信息
        proxy_config = temp["proxy"]
        proxy_path = proxy_config["host"]
        if sitetype == 'jingwai':
            request.meta['proxy'] = proxy_path
        else:
            #获取本地代理
            pass

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def process_exception(self, request, exception, spider):
        pass
