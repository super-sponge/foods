# -*- coding: utf-8 -*-
import scrapy
from foods.utils.comm import FilterLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from foods.utils.comm import loadUrl
from foods.utils.spider.meituan import parse_meituan

import time,json,re


class MeituanSpider(CrawlSpider):
    name = 'meituan'
    allowed_domains = ['meituan.com']
    start_urls = []


    startUrlsFile = "../hlwdata/data/url/meituan_start_url.txt"
    downLoadUrlsFile ="../hlwdata/data/url/meituan_download_url.txt"

    lst = loadUrl(downLoadUrlsFile)
    rules = (
        Rule(FilterLinkExtractor(allow=r'http://cq.meituan.com/shop/[\d]+\.*[\w]*$', download = lst), callback='parse_meituan', process_links =  'link_filtering', follow=True),
    )
    def link_filtering(self, links):
        for link  in links:
            link.url = link.url.rstrip('.html')
        return links;

    def start_requests(self):
        self.start_urls += loadUrl(self.startUrlsFile)
        for url in self.start_urls:
            yield Request(url,callback=self.parse_meituan)
            yield self.make_requests_from_url(url)

    def parse_meituan(self, response):
        with open(self.downLoadUrlsFile, 'a') as f:
            f.write(response.url + '\n')
        item = parse_meituan(response)
        if item:
            return item