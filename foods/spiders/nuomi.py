# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from foods.utils.comm import FilterLinkExtractor
from foods.utils.comm import loadUrl
from foods.utils.spider.nuomi import parse_nuomi

import requests,json,os,re

class NuomiSpider(CrawlSpider):
    name = 'nuomi'
    allowed_domains = ['nuomi.com']
    start_urls = ['http://www.nuomi.com/shop/1482627']

    start_urls = []


    startUrlsFile = "../hlwdata/data/url/nuomi_deal_start_url.txt"
    downLoadUrlsFile ="../hlwdata/data/url/nuomi_deal_download_url.txt"
    downshopUrlsFile ="../hlwdata/data/url/nuomi_shop_download_url.txt"

    lst = loadUrl(downLoadUrlsFile)

    rules = (
        Rule(FilterLinkExtractor(allow=r'http://www.nuomi.com/deal/[\w]+', download = lst), callback='parse_nuomi_deal', follow=True),
        Rule(FilterLinkExtractor(allow=r'http://www.nuomi.com/shop/[\d]+$', download = lst), callback='parse_nuomi_shop', follow=True),
    )

    def start_requests(self):

        for url in loadUrl(self.startUrlsFile):
            yield self.make_requests_from_url(url)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    visitedShop = set(loadUrl(downshopUrlsFile))
    def parse_nuomi_deal(self, response):

        with open(self.downLoadUrlsFile, 'a') as f:
            f.write(response.url + '\n')

        dealId = response.xpath('//div[@class="p-item-info"]/@mon').extract_first().split('=')[1]
        dealUrl = 'http://www.nuomi.com/pcindex/main/shopchain?dealId=' + dealId

        # html = requests.get(dealUrl, headers=self.headers)
        html = requests.get(dealUrl)
        js = json.loads(html.text)
        for shop in js['data']['shop']:
            shopId = shop['merchant_id']
            shoplink = shop['link']
            shopCity = shop['city_id']
            #只获取重庆的美食信息
            # if shopId in self.visitedShop or shopCity != u'900010000':
            if shoplink in self.visitedShop:
                continue
            else:
                self.visitedShop.add(shoplink)
            # yield scrapy.Request(shop['link'], self.parse_nuomi_shop, meta=js['data']['shop'])
            yield scrapy.Request(shoplink, self.parse_nuomi_shop)
    def parse_nuomi_shop(self, response):
        with open(self.downshopUrlsFile, 'a') as f:
            f.write(response.url + '\n')
        # meta = response.meta
        item = parse_nuomi(response)
        if item:
            return item