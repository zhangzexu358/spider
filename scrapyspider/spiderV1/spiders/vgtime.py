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
import urllib


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


class ModelSpider(RedisCrawlSpider):
    name = 'vgtime'

    redis_key = 'vgtime:spider:strat_urls'

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


    def make_requests_from_url(self, url):
        formdatas={
            'category_id':'21',
        }
        return scrapy.FormRequest(url=url,formdata=formdatas,meta={'type':'game'},callback=self.parse_list,dont_filter=True)

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
        type = response.meta["type"]
        jsoninfo = json.loads(obj)
        gameinfo = jsoninfo["data"]
        if "subject_list_group" in gameinfo:
            sublist = gameinfo["subject_list_group"]
            for subject in sublist:
                if "list" in subject:
                    gamelist = subject["list"]
                    for gameinfo in gamelist:
                        item = MovieItem()
                        score = gameinfo["score"]
                        cover = gameinfo["cover_offical"]
                        date = gameinfo["publish_date"]
                        pattern = re.compile('.*(\d{4}-\d{1,2}-\d{1,2}).*')
                        redata = pattern.findall(date)
                        if redata:
                            dateinfo = redata[0]
                            publishtime = dateinfo
                        else:
                            publishtime = '2018-02-23'
                        title = gameinfo["title"]
                        intro = gameinfo["recommend"]
                        id = gameinfo["id"]
                        new_id = "{}_{}".format(self.name,str(id))
                        platforms = list()
                        platform_list = gameinfo["platform_list"]
                        for platforminfo in platform_list:
                            plat_name = platforminfo["title"]
                            platforms.append(plat_name)

                        cover_url = urllib.parse.unquote(cover)
                        item["rate"] = score
                        item["url"] = ""
                        item["tags"] = ""
                        item["cover"] = cover_url
                        item["is_new"] = "False"
                        item["id"] = new_id
                        item["name"] = title
                        item["intro"] = intro
                        item["publishdate"] = publishtime
                        item["data_type"] = "game"
                        item["type"] = type
                        item['platforms']=platforms

                        yield item





