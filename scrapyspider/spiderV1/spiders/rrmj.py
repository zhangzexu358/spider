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
import traceback
import urllib


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"


class ModelSpider(RedisCrawlSpider):
    name = 'rrmj'

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 0,
        'DOWNLOAD_DELAY': 2
    }

    redis_key = 'rrmj:spider:strat_urls'

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

        self.header={
            'p': 'Android',
            'aliId': 'WkkJoM7s+BIDAAfSethXGqmQ',
            'clientType': 'android_Oppo',
            'pkt': 'rrmj',
            'sm': '20180813233705b53bc489fed7c9e91f0691985ecfccce01ef745bb692e47f',
            'clientVersion': '4.4.2',
            'deviceId': '99001245423399',
            'token': '',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A6000 Build/PKQ1.180716.001)',
            'Host': 'api.rr.tv',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            #'Content-Length': 80,
        }
        self.formdata = {
            'simpleBody':'iXOvBFXd462tDmFJSGk2POyMfu202XpXbx9YNju+rGPMYmzR7Qdtne8mnvkhUsrr',
        }
        self.page = 5


    def make_requests_from_url(self, url):
        return scrapy.FormRequest(url=url,formdata=self.formdata,headers=self.header,callback=self.parse_list,dont_filter=True)
        # offset =0
        # pattern = re.compile(r'type=(.*)&tag=', re.S)
        # redata = pattern.findall(url)
        # if redata:
        #     type = redata[0]
        #     new_url = url.format(str(offset))
        #     return scrapy.Request(url=new_url,meta={'original_url':url,'page':1,'type':type},callback=self.parse_list,dont_filter=True)

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
        # original_url = response.meta["original_url"]
        # page = response.meta["page"]
        # type = response.meta["type"]
        jsoninfo = json.loads(obj)
        if "data" in jsoninfo:
            data = jsoninfo["data"]
            if "sections" in data:
                sections = data["sections"]
                for section in sections:
                    display = section["display"]
                    if "TAB_SINGLE" == display :
                        tab_name = section["name"]
                        titleImg = ""
                        if 'titleImg' in section:
                            titleImg = section['titleImg']
                            if titleImg == None:
                                titleImg = ""
                        sectionid = section["id"]
                        newSectionid = 'rrmj_'+str(sectionid)
                        sectionitem = SectionItem()
                        sectionitem['sectionId'] = newSectionid
                        sectionitem['sectionName'] = tab_name
                        sectionitem['sectionImg'] = titleImg
                        sectionitem["data_type"] = "section"

                        yield sectionitem

                        contents = section["content"]
                        if len(contents) > 0:
                            for contentinfo in contents:
                                if "dataList" in contentinfo:
                                    datalist = contentinfo["dataList"]
                                    for datainfo in datalist:
                                        try:
                                            item = MovieItem()
                                            cover = datainfo["cover"]
                                            score = datainfo["score"]
                                            title = datainfo["title"]
                                            isMovie = datainfo["isMovie"]
                                            taglist = list()
                                            if "cat" in datainfo:
                                                cat = datainfo["cat"]
                                                if "/" in cat:
                                                    taglist = cat.split("/")
                                                else:
                                                    taglist.append(cat)
                                            # if "expiredTime" in datainfo:
                                            #     expiredTime = datainfo["expiredTime"]
                                            #     if len(str(expiredTime)) == 13:
                                            #         expiredTime = str(expiredTime)[0:10]
                                            #     timeArray = time.localtime(int(expiredTime))
                                            #     pub_time = time.strftime("%Y-%m-%d", timeArray)
                                            # else:
                                            timeinfo = cover.split('/')[4]
                                            timeArray = time.strptime(timeinfo,'%Y%m%d')
                                            pub_time = time.strftime("%Y-%m-%d", timeArray)
                                            id = datainfo["id"]
                                            new_id = 'rrmj_'+str(id)

                                            item["rate"] = score
                                            item["url"] = ""
                                            item["tags"] = taglist
                                            item["cover"] = cover
                                            item["is_new"] = False
                                            item["id"] = new_id
                                            item["name"] = title
                                            item["intro"] = ''
                                            item["publishdate"] = pub_time
                                            item["data_type"] = "movie"
                                            item["sectionid"] = newSectionid
                                            item['platforms'] = ""
                                            if isMovie:
                                                item["type"] = 'movie'
                                                type = 'movie'
                                            else:
                                                item["type"] = 'tv'
                                                type = 'tv'

                                            pattern = re.compile(r'(第.*季)', re.S)
                                            redata = pattern.findall(title)
                                            if redata:
                                                seasoninfo = redata[0]
                                                title = pattern.sub('', title)
                                                title = str(title).strip() + "+" + str(seasoninfo)
                                            #urllib.parse.quote(title)
                                            search_url = "https://www.douban.com/search?q=%s"%(title)
                                            yield scrapy.Request(url=search_url,meta={'item':item},callback=self.search_movie)


                                            #yield item
                                        except:
                                            traceback.print_exc()
                                            continue
                                else:
                                    try:
                                        datainfo = contentinfo
                                        item = MovieItem()
                                        cover = datainfo["cover"]
                                        score = datainfo["score"]
                                        title = datainfo["title"]
                                        isMovie = datainfo["isMovie"]
                                        taglist = list()
                                        if "cat" in datainfo:
                                            cat = datainfo["cat"]
                                            if "/" in cat:
                                                taglist = cat.split("/")
                                            else:
                                                taglist.append(cat)
                                        # if "expiredTime" in datainfo:
                                        #     expiredTime = datainfo["expiredTime"]
                                        #     if len(str(expiredTime)) == 13:
                                        #         expiredTime = expiredTime[0:10]
                                        #     timeArray = time.localtime(int(expiredTime))
                                        #     pub_time = time.strftime("%Y-%m-%d", timeArray)
                                        # else:
                                        timeinfo = cover.split('/')[4]
                                        timeArray = time.strptime(timeinfo, '%Y%m%d')
                                        pub_time = time.strftime("%Y-%m-%d", timeArray)
                                        id = datainfo["id"]
                                        new_id = 'rrmj_' + str(id)
                                        item["rate"] = score
                                        item["url"] = ""
                                        item["tags"] = taglist
                                        item["cover"] = cover
                                        item["is_new"] = False
                                        item["id"] = new_id
                                        item["name"] =title
                                        item["intro"] = ""
                                        item["publishdate"] = pub_time
                                        item["sectionid"] = newSectionid
                                        item["data_type"] = "movie"
                                        if isMovie:
                                            item["type"] = 'movie'
                                        else:
                                            item["type"] = 'tv'
                                        item['platforms'] = ""

                                        pattern = re.compile(r'(第.*季)', re.S)
                                        redata = pattern.findall(title)
                                        if redata:
                                            seasoninfo = redata[0]
                                            title = pattern.sub('', title)
                                            title = str(title)+"+"+str(seasoninfo)
                                        search_url = "https://www.douban.com/search?q=%s" % (title)
                                        yield scrapy.Request(url=search_url, meta={'item': item},
                                                             callback=self.search_movie)
                                        #yield item
                                    except:
                                        traceback.print_exc()
                                        continue

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
        item = response.meta["item"]
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
                    yield scrapy.Request(url=douban_url, meta={'item':item},callback=self.parse_page)

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

        item = response.meta["item"]

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


        item["url"] = response.url
        item["tags"] = taglist
        item["intro"] = result
        item["publishdate"] = publishtime
        item["data_type"] = "movie"
        item['platforms'] = ""

        yield item

