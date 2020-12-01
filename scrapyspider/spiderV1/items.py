# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class MovieItem(scrapy.Item):
    data_type = scrapy.Field(output_processor=TakeFirst())  # 数据类型（speeches,user）
    url = scrapy.Field(output_processor=TakeFirst())
    tags =  scrapy.Field()
    rate = scrapy.Field(output_processor=TakeFirst())
    cover = scrapy.Field()
    is_new = scrapy.Field(output_processor=TakeFirst())
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    intro = scrapy.Field(output_processor=TakeFirst())
    publishdate = scrapy.Field(output_processor=TakeFirst())
    type = scrapy.Field(output_processor=TakeFirst())
    platforms = scrapy.Field() #
    sectionid = scrapy.Field(output_processor=TakeFirst()) #标签id

class SectionItem(scrapy.Item):
    data_type = scrapy.Field(output_processor=TakeFirst())  # 数据类型（speeches,user）
    sectionId = scrapy.Field(output_processor=TakeFirst())
    sectionName = scrapy.Field(output_processor=TakeFirst())
    sectionImg = scrapy.Field(output_processor=TakeFirst())

