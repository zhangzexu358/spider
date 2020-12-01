import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis.spiders import Spider
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from ..items import *
import time
import random
import json
from scrapy.spiders import Rule
from ..othermodual import siteutil,driverutil
from ..othermodual import siteentity
import re


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


class ModelSpider(RedisCrawlSpider):
    name = 'doubanmovie'

    redis_key = 'doubanmovie:spider:strat_urls'

    site_info = siteutil.get_site_info(name)

    sitebean = siteentity.Site()
    if site_info is not None:
        sitebean = site_info

    site_name = sitebean.sitename
    cookie_info = list()

    # rules = (
    #     Rule(LinkExtractor(allow='https:\/\/theinitium\.com\/article\/.*',),follow=True,callback='parse_page',),
    # )

    def __init__(self,timeout=30, *args, **kwargs):
    #        # Dynamically define the allowed domains list.
        super(ModelSpider, self).__init__(*args, **kwargs)

        need_login = self.sitebean.need_login

        need_driver = self.sitebean.need_webdriver

        self.headers = {
            'Authorization': 'Basic YW5vbnltb3VzOkdpQ2VMRWp4bnFCY1ZwbnA2Y0xzVXZKaWV2dlJRY0FYTHY=',
            'Accept': '*/*',
        }
        self.page = 10


    def make_requests_from_url(self, url):
        offset =0
        pattern = re.compile(r'type=(.*)&tag=', re.S)
        redata = pattern.findall(url)
        if redata:
            type = redata[0]
            new_url = url.format(str(offset))
            return scrapy.Request(url=new_url,meta={'original_url':url,'page':1,'type':type},callback=self.parse_list,dont_filter=True)

    def parse_list(self,response):
        #print(response.url)
        header = response.headers
        encoding = header.encoding
        try:
            obj = response.body.decode(self.sitebean.encoding)
        except Exception as e:
            try:
                obj = response.body.decode(self.sitebean.encoding,"ignore")
            except:
                obj = response.body.decode(encoding, "ignore")
        #offset = response.meta["offset"]
        original_url = response.meta["original_url"]
        page = response.meta["page"]
        type = response.meta["type"]
        jsoninfo = json.loads(obj)
        movielist = jsoninfo["subjects"]
        for movie in movielist:
            rate = movie["rate"]
            url = movie["url"]
            name = movie["title"]
            cover = movie["cover"]
            is_new = movie["is_new"]
            id = movie["id"]
            tmpdata={
                'rate':rate,
                'url':url,
                'name':name,
                'cover':cover,
                'is_new':is_new,
                'id':id,
                'type':type,
            }
            yield scrapy.Request(url=url,meta=tmpdata,callback=self.parse_page)
        if page <= self.page:
            page += 1
            new_offset = (page-1)*20
            new_url = original_url.format(str(new_offset))
            yield scrapy.Request(url=new_url, meta={ 'original_url': original_url, 'page': page,'type':type}, callback=self.parse_list,
                           dont_filter=True)


    def parse_page(self, response):

        # print(response.url)
        #obj = response.body
        obj = ''
        header = response.headers
        encoding = header.encoding
        try:
            obj = response.body.decode(self.sitebean.encoding)
        except Exception as e:
            try:
                obj = response.body.decode(self.sitebean.encoding,"ignore")
            except:
                obj = response.body.decode(encoding, "ignore")

        item = MovieItem()
        movie = response.meta
        rate = movie["rate"]
        url = movie["url"]
        name = movie["name"]
        cover = movie["cover"]
        is_new = movie["is_new"]
        id = movie["id"]
        type=movie["type"]


        data = etree.HTML(obj)

        taglist = data.xpath('//div[@class="article"]//div[@id="info"]//span[@property="v:genre"]//text()')
        introlist = data.xpath('//div[@class="article"]//div[@id="link-report"]//span[@property="v:summary"]//text()')
        intro = ""
        for introinfo in introlist:
            intro += introinfo
        pattern = re.compile(r'<[^>]+>|{[^>]+}|(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', re.S)
        result = pattern.sub('', intro)
        result = result.replace("\r\n", "")
        result = result.replace("\t", "")
        result = result.replace("\n", "")
        result = result.replace("\'", "")
        result = result.strip()
        publishdate = data.xpath('//div[@class="article"]//div[@id="info"]//span[@property="v:initialReleaseDate"]//@content')

        publishtime = ""
        if len(publishdate)>0:
            #pubdate = publishdate[0]
            for date in publishdate:
                pattern = re.compile('.*(\d{4}-\d{1,2}-\d{1,2}).*')
                redata = pattern.findall(date)
                if redata:
                    dateinfo = redata[0]
                    publishtime = dateinfo
                    break
        else:
            publishtime = '2018-02-23'


        item["rate"] = rate
        item["url"] = url
        item["tags"] = taglist
        item["cover"] = cover
        item["is_new"] = is_new
        item["id"] = id
        item["name"] = name
        item["intro"] = result
        item["publishdate"] = publishtime
        item["data_type"] = "movie"
        item["type"] = type
        item['platforms'] = ""

        yield item

