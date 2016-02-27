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


from scrapy import Item,Field
from foods.settings import FIELDS_TO_EXPORT_MEITUAN
from scrapy.http import HtmlResponse

import csv,re,json



import sys,time
reload(sys)
sys.setdefaultencoding('utf8')


class MeituanItem(Item):
    shop_id = Field()  # 商家ID	商家代码
    shop_name = Field()  # 商家名称	商家名称
    shop_adress = Field()  # 商家地址	商家具体地址
    shop_telephone1 = Field()  # 商家电话1	商家联系电话1
    shop_telephone2 = Field()  # 商家电话2	商家联系电话2
    shop_describe = Field()  # 门店介绍	商家门店的具体介绍等信息
    shop_service = Field()  # 门店服务	商家可以提供的WIFI,停车等服务
    speciality = Field()  # 商家特色	商家特色菜品等信息
    shop_hours = Field()  # 营业时间	商家的正常营业时间
    longitude_location = Field()  # 商家经度	商家所属经度
    altitudes_location = Field()  # 商家纬度	商家所属纬度
    shop_type1 = Field()  # 商家大类	大类如：美食、酒店、休闲服务等（目前只有美食）
    shop_type2 = Field()  # 商家小类	小类如：火锅、川菜、西北菜、小吃等
    district = Field()  # 所属区县	江北区、渝北区、忠县、开县等
    street = Field()  # 所属商圈	大学城、解放碑、观影桥、西城天街等
    score = Field()  # 评分	商家的评分（1-5分）
    consume_number = Field()  # 消费人数	商家累计消费人数
    evaluate_number = Field()  # 评价人数	商家累计评价人数
    shop_photo = Field()  # 商家图片	商家门店宣传图片
    input_time = Field()  # 爬取时间	数据首次爬取时间
    update_time = Field()  # 更新时间	数据更新时间--暂可为空
    data_source = Field()  # 数据来源	美团


#解析文本内容
def parse_meituan(response):

    sel = response.xpath('//div[@data-component="bread-nav"]')
    tag = sel.xpath('div/a[@gaevent="crumb/index"]/text()').extract_first()
    if tag != u'重庆美食':
            # with open(self.downLoadUrlsFile, 'a') as f:
            #     f.write(response.url + '\n')
        return None

    item = MeituanItem()
    item['shop_type1']= sel.xpath('div/a[@gaevent="crumb/category/1"]/text()').extract_first()
    item['shop_type2']= sel.xpath('div/a[@gaevent="crumb/category/2"]/text()').extract_first()
    item['district']= sel.xpath('div/a[@gaevent="crumb/area/1"]/text()').extract_first()
    item['street']= sel.xpath('div/a[@gaevent="crumb/area/2"]/text()').extract_first()
    item['score']=response.xpath('//span[@class="biz-level"]/strong/text()').extract_first()
    item['consume_number']= response.xpath('//div[@class="counts"]/div/span[@class="num"]/text()').extract_first()
    item['evaluate_number']=response.xpath('//div[@class="counts"]/div/a[@class="num rate-count"]/text()').extract_first()
    item['shop_photo']=''
    item['input_time']= time.strftime('%Y-%m-%d %H:%M:%S')

    sel = response.xpath('//div[@class="fs-section__left"]')

    shopId = re.search(r'/shop/([\d]+)$', response.url).group(1)

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

    item['shop_id'] = shopId
    item['shop_name'] = shopName.strip('\n').strip(' ').strip('\n')
    item['shop_adress'] = shopAddr.strip('\n').strip(' ').strip('\n')
    item['shop_telephone1'] = shopPhone
    item['longitude_location'] = shopGlng
    item['altitudes_location'] = shopGlat

    item['data_source'] = shopUrl

    item['shop_telephone2'] = ''
    item['shop_describe'] = ''
    item['shop_service'] = ''
    item['speciality'] = ''
    item['shop_hours'] = ''
    item['update_time'] = ''

        # with open(self.downLoadUrlsFile, 'a') as f:
        #     f.write(response.url + '\n')


    return item


def saveItem(htmlfile, writer):
    html = ''
    with open(htmlfile) as f:
        html = f.read()
    url = 'http://cq.meituan.com/shop/' + htmlfile.split('.')[-2]
    response = HtmlResponse(url=url,body=html)
    item = parse_meituan(response)
    if item:
        row = []
        for id in FIELDS_TO_EXPORT_MEITUAN:
            row.append(item[id])
        writer.writerow(row)



if __name__ == '__main__':
    outFile = "../hlwdata/data/meituan_new_page.csv"
    infilelst = '../hlwdata/data/url/meituan_page_index.txt'


    csvfile = file(outFile, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(FIELDS_TO_EXPORT_MEITUAN)

    for line in open(infilelst).readlines():
        saveItem(line.rstrip('\n'), writer)

    csvfile.close()


