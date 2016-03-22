# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item, Field
from scrapy.http import Request
import re


class DianPingReviewItem(Item):
    shop_id = Field() #商家ID
    user_id = Field() #评论用户ID
    user_name = Field() #评论用户名
    review_star = Field() #评论星级
    review_Content = Field() #评论内容
    review_date = Field() #评论时间

class DianpingreviewSpider(scrapy.Spider):
    name = "dianpingreview"
    allowed_domains = ["dianping.com"]
    start_urls = (
        'https://www.dianping.com/shop/20919783/review_more',
        'https://www.dianping.com/shop/18506539/review_more'
    )

    def parse(self, response):
        print response.url;

        shop_id = re.search(r'/shop/([\d]+)/review_more', response.url).group(1)
        for comment in response.xpath('//div[@class="comment-list"]/ul/li'):
            item = DianPingReviewItem()
            item['shop_id'] = shop_id
            item['user_id'] = comment.xpath('./div[@class="pic"]/a/@user-id').extract()
            item['user_name'] = comment.xpath('./div[@class="pic"]/p[@class="name"]/a/text()').extract()
            item['review_star'] = comment.xpath('./div[@class="content"]/div[@class="user-info"]/span/@class').extract()
            item['review_Content'] = comment.xpath('./div[@class="content"]/div[@class="comment-txt"]/div/text()').extract()
            item['review_date'] = comment.xpath('./div[@class="content"]/div[@class="misc-info"]/span[@class="time"]/text()').extract()
            yield  item

        nextPages = response.xpath('//div[@class="Pages"]/div[@class="Pages"]/a[@class="NextPage"]/@href').extract_first()

        if nextPages:
            yield Request(response.url.split('?')[0] + nextPages, dont_filter=True,callback= self.parse)
