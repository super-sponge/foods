# -*- coding: utf-8 -*-
import scrapy
from foods.utils.comm import FilterLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from foods.utils.spider.dianping import parse_dianping

from foods.utils.comm import loadUrl


class DianpingSpider(CrawlSpider):
    name = 'dianping'
    allowed_domains = ['dianping.com']
    start_urls = []

    startUrlsFile = "../hlwdata/data/url/dianping_start_url.txt"
    downLoadUrlsFile ="../hlwdata/data/url/dianping_download_url.txt"

    lst = loadUrl(downLoadUrlsFile)
    rules = (
        Rule(FilterLinkExtractor(allow=r'https://www.dianping.com/shop/[\d]+$', download = lst), callback='parse_dianping', follow=True),
    )

    def start_requests(self):

        for url in loadUrl(self.startUrlsFile):
            yield self.make_requests_from_url(url)
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_dianping(self, response):
        with open(self.downLoadUrlsFile, 'a') as f:
            f.write(response.url + '\n')
        item = parse_dianping(response)
        if item:
            return item