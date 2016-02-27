# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider, Rule
# from scrapy.utils.project import get_project_settings

from foods.items import ShopIndexItem

import requests, json, re

from foods.utils.comm import loadUrl
from foods.utils.comm import FilterLinkExtractor
from foods.utils.comm import headers

class ShopindexSpider(CrawlSpider):
    name = 'shopindex'
    allowed_domains = ['nuomi.com', 'dianping.com','cq.meituan.com']
    start_urls = [
                 # 'https://www.dianping.com/shop/24098260'
                  # 'http://cq.meituan.com/shop/82458075'
                  # ,'http://www.nuomi.com/deal/d3ccslof.html'
                  # ,'https://www.dianping.com/shop/32463358'
                  ]

    # settings = get_project_settings()

    downLoadUrlsFile = '../hlwdata/data/start_url.txt'
    startUrlsFile = '../hlwdata/data/downloaded_url.txt'
    lst = loadUrl(downLoadUrlsFile)

    rules = (
        Rule(FilterLinkExtractor(allow=r'http://www.nuomi.com/deal/[\w]+', download = lst), callback='parse_nuomi', follow=True),
        Rule(FilterLinkExtractor(allow=r'https://www.dianping.com/shop/[\d]+$', download = lst), callback='parse_dianping', follow=True),
        Rule(FilterLinkExtractor(allow=r'http://cq.meituan.com/shop/[\d]+\.*[\w]*$', download = lst), callback='parse_meituan', process_links =  'link_filtering', follow=True),
    )




    def link_filtering(self, links):
        for link  in links:
            link.url = link.url.rstrip('.html')
        return links;

    visitedShop = set()
    def start_requests(self):

        for url in loadUrl(self.startUrlsFile):
            yield self.make_requests_from_url(url)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)


    def parse_nuomi(self, response):

        #只爬取美食类信息
        prdType = response.xpath('//div[@class="w-bread-crumb"]//a[@href="/326"]/text()').extract()
        prdType = "".join(prdType).strip('\n')
        if prdType != u'美食':
            return

        items = []
        sel = response.xpath('//div[@class="p-item-info"]')
        dealId = sel.xpath('@mon').extract_first().split('=')[1]
        shopUrl = 'http://www.nuomi.com/pcindex/main/shopchain?dealId=' + dealId

        html = requests.get(shopUrl, headers=headers)

        js = json.loads(html.text)

        # shopCity = js['data']['city']['900010000']['city_name']

        for shop in js['data']['shop']:

            shopId = shop['merchant_id']
            shopCity = shop['city_id']
            #只获取重庆的美食信息
            # if shopId in self.visitedShop or shopCity != u'900010000':
            if shopId in self.visitedShop:
                continue
            else:
                self.visitedShop.add(shopId)
            shopName = shop['name']
            shopCity = js['data']['city'][shopCity]['city_name']
            shopAddr = shop['address']
            shopPhone = shop['phone']
            shopGlat = shop['baidu_latitude']
            shopGlng = shop['baidu_longitude']
            shopUrl = shop['link']
            shopPicSave = ''
            shopScrapWeb = 'nuomi'

            item = ShopIndexItem()
            item['shopId'] = shopId
            item['shopCity'] = shopCity
            item['shopName'] = shopName
            item['shopAddr'] = shopAddr
            item['shopPhone'] = shopPhone
            item['shopGlat'] = shopGlat
            item['shopGlng'] = shopGlng
            item['shopUrl'] = shopUrl
            item['shopPicSave'] = shopPicSave
            item['shopScrapWeb'] = shopScrapWeb

            items.append(item)
        return items

    def parse_dianping(self, response):
        sel = response.xpath('//div[@id="basic-info"]')

        #只爬取美食类信息, 有如上标记，判断为美食信息

        if not sel :
            print 'not meishi ' + response.url
            return

        shopId = re.search(r'/shop/([\d]+)$', response.url).group(1)

        if shopId in self.visitedShop:
            return
        else:
            self.visitedShop.add(shopId)

        shopCity = response.xpath('//*[@id="page-header"]//a[@class="city J-city"]/text()').extract_first()
        shopName = sel.xpath('h1[@class="shop-name"]/text()').extract_first()
        shopAddr = sel.xpath('.//span[@itemprop="street-address"]/text()').extract_first()
        shopPhone = sel.xpath('.//span[@itemprop="tel"]/text()').extract_first()

        # shopDataUrl = 'http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP?shopId=%s'%shopId
        # htmlshop = requests.get(shopDataUrl, headers= headers)
        # try:
        #     shopJson = json.loads(htmlshop.text)
        #     shopInfo = shopJson['msg']['shopInfo']
        #     shopGlat = str(shopInfo['glat'])
        #     shopGlng = str(shopInfo['glng'])
        #
        # except (ValueError, KeyError, TypeError):
        #     print "JSON format error"
        shopInfo =''
        lng = re.search(r'lng:([\d]+\.[\d]+)', response.body)
        lat = re.search(r'lat:([\d]+\.[\d]+)', response.body)
        shopGlat= ''
        shopGlng= ''
        if lng and lat:
            shopGlng= lng.group(1)
            shopGlat= lat.group(1)

        shopUrl = response.url
        shopPicSave = ''
        shopScrapWeb = 'dianping'

        item = ShopIndexItem()
        item['shopId'] = shopId
        item['shopCity'] = shopCity
        item['shopName'] = shopName.strip('\n').strip(' ').strip('\n')
        item['shopAddr'] = shopAddr.strip('\n').strip(' ').strip('\n')
        item['shopPhone'] = shopPhone
        item['shopGlat'] = shopGlat
        item['shopGlng'] = shopGlng
        item['shopUrl'] = shopUrl
        item['shopPicSave'] = shopPicSave
        item['shopScrapWeb'] = shopScrapWeb

        yield item

    def parse_meituan(self, response):
        sel = response.xpath('//div[@class="fs-section__left"]')

        # if not response.xpath('//div[@id="meishi-menu"]/h2[@class="content-title"]'):
        #     print 'not meishi ' + response.url
        #     return

        shopId = re.search(r'/shop/([\d]+)$', response.url).group(1)
        if shopId in self.visitedShop:
            return
        else:
            self.visitedShop.add(shopId)

        shopName = sel.xpath('.//h2/span[@class="title"]/text()').extract_first()
        shopAddr = sel.xpath('.//p/span[@class="geo"]/text()').extract_first()

        shopJson = json.loads(sel.xpath('.//p/span[@id="map-canvas"]/@data-params').extract_first())
        shopInfo = shopJson['shops'][shopId]
        shopPhone = shopInfo['phone']
        shopGlat = str(shopInfo['position'][0])
        shopGlng = str(shopInfo['position'][1])

        shopUrl = response.url
        shopPicSave = ''
        shopScrapWeb = 'meituan'

        item = ShopIndexItem()
        item['shopId'] = shopId
        item['shopCity'] = ''
        item['shopName'] = shopName.strip('\n').strip(' ').strip('\n')
        item['shopAddr'] = shopAddr.strip('\n').strip(' ').strip('\n')
        item['shopPhone'] = shopPhone
        item['shopGlat'] = shopGlat
        item['shopGlng'] = shopGlng
        item['shopUrl'] = shopUrl
        item['shopPicSave'] = shopPicSave
        item['shopScrapWeb'] = shopScrapWeb

        yield item


