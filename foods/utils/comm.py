#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: 刘红波
@license: ***
@contact: super_sponge@163.com
@see: https://github.com/super-sponge

@version: 0.0.1
@todo[0.0.2]: a new module

@note: a comment
@attention: please attention
@bug: a exist bug
@warning: warnings
'''

import os
from scrapy.linkextractors import  LinkExtractor


headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36'
    }



def loadUrl(urlFile):
    result = set()
    if os.path.exists(urlFile):
        with open(urlFile, 'r+') as f:
            for line in f.readlines():
                line = line.strip('\n')
                result.add(line)
    return result


class FilterLinkExtractor(LinkExtractor):
    def __init__(self, allow=(), download = set()):
        super(FilterLinkExtractor, self).__init__(allow=allow)
        self.downloaded = download

    def extract_links(self, response):
        result = []
        for link in super(FilterLinkExtractor, self).extract_links(response):
            if link.url.rstrip('.html') not in self.downloaded and link.url not in self.downloaded:
                result.append(link)
            else:
                print "Exists  %s" % link.url
        return result
#     file1 - file2 列表1比列表2多的元素
def cmpIndex(file1, file2):
    lst1 = open(file1).read().split('\n')
    lst2 = open(file2).read().split('\n')

    result = []
    for url in lst1:
        if url not in lst2:
            result.append(url)

    return result


if __name__ == '__main__':
    # urls = loadUrl('/home/sponge/scrapy/foods/data/start_url.txt')

    # lst = cmpIndex('/home/sponge/scrapy/foods/data/downloaded_url.txt',
    #          '/home/sponge/scrapy/foods/data/start_url.txt')
    # f = open('/home/sponge/scrapy/foods/data/downloaded_url.txt', 'w')
    # for url in set(lst):
    #     f.write(url + '\n')
    #
    lst = cmpIndex('/home/sponge/scrapy/hlwdata/data/meituan_download_url.txt',
             '/home/sponge/scrapy/hlwdata/data/meituan_start_url.url')
    f = open('/home/sponge/scrapy/hlwdata/data/meituan_download_url.url', 'w')
    for url in set(lst):
        f.write(url + '\n')

