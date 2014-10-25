# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pn=scrapy.Field()  #包名
    cls=scrapy.Field() #分类
    isc=scrapy.Field() #安装量
