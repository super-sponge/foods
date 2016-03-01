# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from foods.utils.comm import FilterLinkExtractor
from foods.utils.comm import loadUrl
from foods.utils.spider.nuomi import parse_nuomi
from scrapy.http import Request

import requests,json,os,re

class NuomiSpider(CrawlSpider):
    name = 'nuomi'
    allowed_domains = ['nuomi.com']
    start_urls = []


    startUrlsFile = "../hlwdata/data/url/nuomi_deal_start_url.txt"
    downLoadUrlsFile ="../hlwdata/data/url/nuomi_deal_download_url.txt"
    downshopUrlsFile ="../hlwdata/data/url/nuomi_shop_download_url.txt"
    jsonDir ="../hlwdata/data/json/nuomi/shop/"
    jsonDir ="../hlwdata/data/json/nuomi/city/"

    lst = loadUrl(downLoadUrlsFile)

    rules = (
        Rule(FilterLinkExtractor(allow=r'http://www.nuomi.com/deal/[\w]+', download = lst), callback='parse_nuomi_deal', follow=True),
        # Rule(FilterLinkExtractor(allow=r'http://www.nuomi.com/shop/[\d]+$', download = lst), callback='parse_nuomi_shop', follow=True),
    )

    def start_requests(self):
        self.start_urls += loadUrl(self.startUrlsFile)
        for url in self.start_urls:
            yield Request(url,callback=self.parse_nuomi_deal)
            yield self.make_requests_from_url(url)


    visitedShop = set(loadUrl(downshopUrlsFile))
    def parse_nuomi_deal(self, response):

        with open(self.downLoadUrlsFile, 'a') as f:
            f.write(response.url + '\n')
        navs = response.xpath('//div[@class="w-bread-crumb"]/ul[@class="crumb-list clearfix"]/li/a/text()').extract()
        parmeta = dict()
        parmeta['nav'] = True
        parmeta['deal'] = response.url
        for i in range(6):
            parmeta['nav' + str(i)] = ''
        for i in range(len(navs)):
            parmeta['nav' + str(i)] = navs[i].strip('\n')

        dealId = response.xpath('//div[@class="p-item-info"]/@mon').extract_first().split('=')[1]
        dealUrl = 'http://www.nuomi.com/pcindex/main/shopchain?dealId=' + dealId

        # html = requests.get(dealUrl, headers=self.headers)
        # js['data']['city'][shopCity]
        html = requests.get(dealUrl)
        js = json.loads(html.text)
        for shop in js['data']['shop']:
            shopCity = shop['city_id']
            district_id = shop['district_id']
            shopId = shop['merchant_id']
            with open(self.jsonDir + shopId, 'w') as f:
                f.write(json.dumps(shop))
            with open(self.jsonDir + shopId + '.' + shopCity, 'w') as f:
                f.write(json.dumps(js['data']['city'][shopCity]))

            shoplink = shop['link']
            #只获取重庆的美食信息
            # if shopId in self.visitedShop or shopCity != u'900010000':
            if shoplink in self.visitedShop:
                continue
            else:
                self.visitedShop.add(shoplink)
            city = js['data']['city'][shopCity]
            shopCityName = city['city_name']
            district = city['district'][district_id]['dist_name']

            parmeta['shopCityName'] = shopCityName
            parmeta['district'] = district


            yield scrapy.Request(shop['link'], self.parse_nuomi_shop, meta=parmeta)
    def parse_nuomi_shop(self, response):
        with open(self.downshopUrlsFile, 'a') as f:
            f.write(response.url + '\n')
        meta = response.meta
        item = parse_nuomi(response, meta =response.meta)
        if item:
            return item