# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ShopIndexItem(scrapy.Item):
    shopId = scrapy.Field()  # 商店ID
    shopCity = scrapy.Field()  # 商店所在城市
    shopName = scrapy.Field()  # 商店名称
    shopAddr = scrapy.Field()  # 商店地址
    shopPhone = scrapy.Field()  # 商店电话
    shopGlat = scrapy.Field()  # 商店经度
    shopGlng = scrapy.Field()  # 商店维度
    shopUrl = scrapy.Field()  # 商店网址
    shopPicSave = scrapy.Field()  # 商店图片存放地址
    shopScrapWeb = scrapy.Field()  # 抓取网站
