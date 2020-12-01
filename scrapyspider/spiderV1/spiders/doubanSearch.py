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
    name = 'doubanSearch'

    redis_key = 'doubanSearch:spider:strat_urls'

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
        self.page = 5


    def make_requests_from_url(self, data:str):
        datajson = json.loads(data)
        movie_name = datajson["name"]
        movie_id = datajson["id"]
        type = datajson["type"]
        sectionid = datajson["sectionid"]
        search_url = "https://www.douban.com/search?q=%s" % (movie_name)
        return scrapy.Request(url=search_url, meta={'id':movie_id,'name':movie_name,'type':type,'sectionid':sectionid}, callback=self.search_movie,dont_filter=True)

    def search_movie(self,response):
        header = response.headers
        encoding = header.encoding
        try:
            obj = response.body.decode(self.sitebean.encoding)
        except Exception as e:
            try:
                obj = response.body.decode(self.sitebean.encoding, "ignore")
            except:
                obj = response.body.decode(encoding, "ignore")
        # offset = response.meta["offset"]
        # movie_id = response.meta["id"]
        # movie_name = response.meta["name"]
        # type = response.meta["type"]
        data = etree.HTML(obj)
        resultlist = data.xpath('//div[@class="result-list"]//div[@class="result"]')
        if len(resultlist) > 0:
            resultinfo = resultlist[0]
            clickinfo = resultinfo.xpath('.//div[@class="content"]//div[@class="title"]//h3//a/@onclick')
            if len(clickinfo) > 0:
                click = clickinfo[0]
                pattern = re.compile(r'sid: (\d*),', re.S)
                redata = pattern.findall(click)
                if redata:
                    doubanId = redata[0]
                    douban_url = "https://movie.douban.com/subject/%s/" % (doubanId)
                    yield scrapy.Request(url=douban_url, meta=response.meta,callback=self.parse_page)

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

        movie_id = response.meta["id"]
        movie_name = response.meta["name"]
        type = response.meta["type"]
        sectionid = response.meta["sectionid"]

        item = MovieItem()

        data = etree.HTML(obj)

        taglist = data.xpath('//div[@class="article"]//div[@id="info"]//span[@property="v:genre"]//text()')
        introlist = data.xpath('//div[@class="article"]//div[@id="link-report"]//span[@property="v:summary"]//text()')
        scoreinfo = data.xpath('//div[@class="article"]//strong[@property="v:average"]//text()')
        imgurl = data.xpath('//div[@class="article"]//div[@id="mainpic"]//img/@src')
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

        score = "0"
        if len(scoreinfo) > 0:
            score = str(scoreinfo[0])
        cover=""
        if len(imgurl)>0:
            cover = imgurl[0]


        item["rate"] = score
        item["url"] = response.url
        item["cover"] = cover
        item["is_new"] = False
        item["tags"] = taglist
        item["intro"] = result
        item["publishdate"] = publishtime
        item["data_type"] = 'movie'
        item["name"] = movie_name
        item["id"] = movie_id
        item["type"] = type
        item["sectionid"] = sectionid
        item['platforms'] = ""

        yield item




